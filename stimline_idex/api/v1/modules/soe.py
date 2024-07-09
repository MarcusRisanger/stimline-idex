from typing import Optional, overload

from ....data_schemas import str
from ....data_schemas.v1.assets import Wellbore
from ....data_schemas.v1.events import (
    SoeActivity,
    SoeChemicalMeasurement,
    SoeJob,
    SoeTask,
)
from ..api import IDEXApi


class Soe:
    def __init__(self, api: IDEXApi) -> None:
        self._api = api

    def _get_jobs(self, wellbore_id: str) -> list[SoeJob]:
        wellbore_id = str(wellbore_id)
        data = self._api.get(url=f"SequenceOfEvents/{wellbore_id}/Jobs")
        if data.status_code == 204:
            return []

        return [SoeJob.model_validate(row) for row in data.json()]

    def _get_tasks(self, wellbore_id: str, job_id: str) -> list[SoeTask]:
        wellbore_id, job_id = str(wellbore_id), str(job_id)
        data = self._api.get(url=f"SequenceOfEvents/{wellbore_id}/Jobs/{job_id}/Tasks")
        if data.status_code == 204:
            return []  # Empty response

        tasks = [SoeTask.model_validate(row) for row in data.json()]
        for task in tasks:  # Enriching with wellbore_id, not part of API payload
            task.wellbore_id = wellbore_id
        return tasks

    def _get_chemical_measurements(self, wellbore_id: str, job_id: str) -> list[SoeChemicalMeasurement]:
        wellbore_id, job_id = str(wellbore_id), str(job_id)
        data = self._api.get(url=f"SequenceOfEvents/{wellbore_id}/Jobs/{job_id}/ChemicalMeasurements")
        if data.status_code == 204:
            return []

        measurements = [SoeChemicalMeasurement.model_validate(row) for row in data.json()]
        for measurement in measurements:
            measurement.wellbore_id = wellbore_id
        return measurements

    def _get_activities(self, wellbore_id: str, job_id: str, task_id: str) -> list[SoeActivity]:
        wellbore_id, job_id, task_id = str(wellbore_id), str(job_id), str(task_id)
        data = self._api.get(url=f"SequenceOfEvents/{wellbore_id}/Jobs/{job_id}/Tasks/{task_id}/Activities")
        if data.status_code == 204:
            return []

        return [SoeActivity.model_validate(row) for row in data.json()]

    @overload
    def get_jobs(self, *, wellbore: Wellbore) -> list[SoeJob]: ...
    @overload
    def get_jobs(self, *, wellbore_id: str) -> list[SoeJob]: ...

    def get_jobs(self, *, wellbore: Optional[Wellbore] = None, wellbore_id: Optional[str] = None) -> list[SoeJob]:
        """
        Get all SoE Jobs for a given Wellbore.

        Parameters
        ----------
        wellbore : Wellbore
            The Wellbore object for which to retrieve all Jobs.
        wellbore_id : IdType
            The UUID of the Wellbore for which to retrieve all Jobs.

        Returns
        -------
        list[SoeJob]
            A list of SoeJob objects for the Wellbore.

        """
        if all(v is None for v in [wellbore, wellbore_id]):
            raise ValueError("Provide only one of: wellbore, wellbore_id.")
        if wellbore is not None:
            return self._get_jobs(wellbore_id=wellbore.id)
        if wellbore_id is not None:
            return self._get_jobs(wellbore_id=wellbore_id)  # type: ignore

        raise ValueError("Either wellbore or wellbore_id must be provided.")

    @overload
    def get_tasks(self, *, job: SoeJob) -> list[SoeTask]: ...
    @overload
    def get_tasks(self, *, wellbore_id: str, job_id: str) -> list[SoeTask]: ...

    def get_tasks(
        self, *, job: Optional[SoeJob] = None, wellbore_id: Optional[str] = None, job_id: Optional[str] = None
    ) -> list[SoeTask]:
        """
        Get all Tasks for a given SoE Job.

        Use either a SoeJob object or provide the wellbore_id and job_id explicitly.

        Parameters
        ----------
        job : SoeJob
            The SoeJob object for which to retrieve all Tasks.
        wellbore_id : IdType
            The UUID of the Wellbore for which to retrieve all Tasks.
        job_id : IdType
            The UUID of the Job for which to retrieve all Tasks.

        Returns
        -------
        list[SoeTask]
            A list of SoeTask objects for the Job.

        """
        if all(v is not None for v in [job, wellbore_id, job_id]):
            raise ValueError("Either job or wellbore_id and job_id must be provided, not both.")
        if job is not None:
            return self._get_tasks(wellbore_id=job.wellbore_id, job_id=job.id)
        if wellbore_id is not None and job_id is not None:
            return self._get_tasks(wellbore_id=wellbore_id, job_id=job_id)

        raise ValueError("Either job or wellbore_id and job_id must be provided.")

    @overload
    def get_chemical_measurements(self, *, job: SoeJob) -> list[SoeChemicalMeasurement]: ...
    @overload
    def get_chemical_measurements(self, *, wellbore_id: str, job_id: str) -> list[SoeChemicalMeasurement]: ...

    def get_chemical_measurements(
        self, *, job: Optional[SoeJob] = None, wellbore_id: Optional[str] = None, job_id: Optional[str] = None
    ) -> list[SoeChemicalMeasurement]:
        """
        Get all Chemical Measurements for a given SoE Job.

        Use either a SoeJob object or provide the wellbore_id and job_id explicitly.

        Parameters
        ----------
        job : SoeJob
            The SoeJob object for which to retrieve all Chemical Measurements.
        wellbore_id : IdType
            The UUID of the Wellbore for which to retrieve all Chemical Measurements.
        job_id : IdType
            The UUID of the Job for which to retrieve all Chemical Measurements.

        Returns
        -------
        list[SoeChemicalMeasurement]
            A list of `SoeChemicalMeasurement` objects for the Job.

        """
        if job is not None and any(v is not None for v in [wellbore_id, job_id]):
            raise ValueError("Either job or wellbore_id and job_id must be provided, not both.")
        if job is not None:
            return self._get_chemical_measurements(wellbore_id=job.wellbore_id, job_id=job.id)
        if all(v is not None for v in [wellbore_id, job_id]):
            return self._get_chemical_measurements(wellbore_id=wellbore_id, job_id=job_id)  # type: ignore

        raise ValueError("Either job or wellbore_id and job_id must be provided.")

    @overload
    def get_activities(self, *, task: SoeTask) -> list[SoeActivity]: ...
    @overload
    def get_activities(self, *, wellbore_id: str, job_id: str, task_id: str) -> list[SoeActivity]: ...

    def get_activities(
        self,
        *,
        task: Optional[SoeTask] = None,
        wellbore_id: Optional[str] = None,
        job_id: Optional[str] = None,
        task_id: Optional[str] = None,
    ) -> list[SoeActivity]:
        """
        Get all Activities for a given SoE Job Task.

        Use either a SoeTask object or provide the wellbore_id, job_id and task_id explicitly.

        Parameters
        ----------
        job : SoeJob
            The SoeJob object for which to retrieve all Chemical Measurements.
        wellbore_id : IdType
            The UUID of the Wellbore for which to retrieve all Chemical Measurements.
        job_id : IdType
            The UUID of the Job for which to retrieve all Chemical Measurements.
        task_id : IdType
            The UUID of the Task for which to retrieve all Activities.

        Returns
        -------
        list[SoeActivity]
            A list of `SoeActivity` objects for the Task.

        """
        if task is not None and any(v is not None for v in [task, wellbore_id, job_id, task_id]):
            raise ValueError("Provide either a `SoeTask` or a wellbore_id, job_id, and task_id combination.")
        if task is not None:
            return self._get_activities(wellbore_id=task.wellbore_id, job_id=task.job_id, task_id=task.id)  # type: ignore
        if all(v is not None for v in [wellbore_id, job_id, task_id]):
            return self._get_activities(wellbore_id=wellbore_id, job_id=job_id, task_id=task_id)  # type: ignore

        raise ValueError("Provide either a `SoeTask` or a wellbore_id, job_id, and task_id combination.")
