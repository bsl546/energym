class KPI(object):
    """A class to track the KPIs while running simulations.

    The KPIs are customizable by specifying them in the kpi_options dict.
    An example for the dict looks as follows:

    kpi_options = {

        "kpi1":{"name":"Z01_T" ,"type":"avg_dev", "target":[19,23]},

        "kpi2":{"name":"Z01_T" ,"type":"tot_viol", "target":[19,23]},

        "kpi3":{"name":"Fa_Pw_All","type":"avg"},

        "kpi4":{"name":"Fa_Pw_All", "type":"sum"}

    }

    Possible KPI types are:
        * "avg": The average over the given steps.
        * "sum": The sum over the given steps.
        * "avg_dev": The average deviation from a target (float or list).
        * "tot_viol": The number of interval constraint violations for a
            target interval (list).

    Attributes
    ----------
    kpi_dict: dict
        Dict of kpi related outputs with list of observations
    num_obs: int
        Number of saved observations

    Methods
    -------
    add_observations(obs)
        Extracts relevant observations and appends them to the
        corresponding list.
    get_kpi(start_ind, end_ind)
        Computes the KPIs for a given time window.
    get_cumulative_kpi(phrase, kpi_type, out_type)
        Computes cumulative KPIs over multiple variables.
    reset()
        Frees up the storages in the object.
    """

    def __init__(self, kpi_options):
        """
        Parameters
        ----------
        kpi_options : dict
            Dict to specify the tracked KPIs.
        """
        self.kpi_options = kpi_options
        self._initialize_kpi_dict()
        self.num_obs = 0

    def _initialize_kpi_dict(self):
        self.kpi_dict = {}
        for key in self.kpi_options:
            self.kpi_dict[key] = []

    def add_observation(self, obs):
        """Extracts relevant observations and appends them to the corresponding list.

        Parameters
        ----------
        obs : dict
            Observation object to be tracked.
        """
        added_obs = 0
        for key in self.kpi_options:
            if type(obs[self.kpi_options[key]["name"]]) == list:
                self.kpi_dict[key].extend(
                    obs[self.kpi_options[key]["name"]]
                )
                added_obs = len(obs[self.kpi_options[key]["name"]])
            else:
                self.kpi_dict[key].append(
                    obs[self.kpi_options[key]["name"]]
                )
                added_obs = 1
        self.num_obs = self.num_obs + added_obs

    def get_kpi(self, start_ind=0, end_ind=-1):
        """Computes the KPIs for a given time window.

        Parameters
        ----------
        start_ind : int, optional
            Index determining the start of the time window, by default 0
        end_ind : int, optional
            Index determining the end of the time window, by default -1

        Returns
        -------
        kpi_summary : dict
            Dict containing the KPIs.

        Raises
        ------
        IndexError
            If no observations are stored.
        """
        if self.num_obs == 0:
            raise IndexError("Can't compute KPIs without observations!")
        else:
            if end_ind > self.num_obs:
                end_ind = self.num_obs
            elif end_ind < 0:
                end_ind = self.num_obs + 1 + end_ind
            if start_ind < 0:
                start_ind = self.num_obs + start_ind
            assert start_ind < end_ind
            kpi_summary = self.kpi_options.copy()
            for key in self.kpi_options:
                kpi_val = self._compute_kpi(
                    self.kpi_dict[key][start_ind:end_ind],
                    self.kpi_options[key],
                    end_ind - start_ind,
                )
                kpi_summary[key]["kpi"] = kpi_val
            return kpi_summary

    def _compute_kpi(self, obs, opts, length):
        if opts["type"] == "avg":
            obs_abs = map(abs, obs)
            kpi = sum(obs_abs) / length
        elif opts["type"] == "sum":
            kpi = sum(obs)
        elif opts["type"] == "avg_dev":
            kpi = 0
            if type(opts["target"]) == list:
                for val in obs:
                    if val < opts["target"][0]:
                        kpi += opts["target"][0] - val
                    elif val > opts["target"][1]:
                        kpi += val - opts["target"][1]
            else:
                for val in obs:
                    kpi += abs(val - opts["target"])
            kpi = kpi / length
        elif opts["type"] == "tot_viol":
            kpi = 0
            for val in obs:
                if val < opts["target"][0] or val > opts["target"][1]:
                    kpi += 1
        return kpi

    def get_cumulative_kpi(self, names, kpi_type, out_type):
        """Computes cumulative KPIs over multiple variables.

        Parameters
        ----------
        names : list or str
            List of variable names or common string to filter the variables.
        kpi_type : str
            One of the 4 KPI types to filter the variables.
        out_type : str
            Cumulative KPI type ("avg" or "sum").

        Returns
        -------
        float or int
            Cumulative KPI value.

        Raises
        ------
        IndexError
            If no variables fitting the criteria are detected.
        """
        cumulative_kpi = 0
        num = 0
        kpi_summary = self.get_kpi()
        if isinstance(names, list):
            for key in kpi_summary:
                for name in names:
                    if (
                        name == kpi_summary[key]["name"]
                        and kpi_summary[key]["type"] == kpi_type
                    ):
                        cumulative_kpi += kpi_summary[key]["kpi"]
                        num += 1
        else:
            for key in kpi_summary:
                if (
                    names in kpi_summary[key]["name"]
                    and kpi_summary[key]["type"] == kpi_type
                ):
                    cumulative_kpi += kpi_summary[key]["kpi"]
                    num += 1
        if num == 0:
            raise IndexError(
                "No KPIs corresponding to {} found!".format(names)
            )
        if out_type == "avg":
            cumulative_kpi = cumulative_kpi / num
        return cumulative_kpi

    def reset(self):
        """Frees up the storages in the object."""
        self.num_obs = 0
        for key in self.kpi_dict:
            self.kpi_dict[key] = []
