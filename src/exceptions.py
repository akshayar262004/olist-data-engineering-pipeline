
class PipelineError(Exception):
    pass


class DatasetNotFoundError(PipelineError):
    pass


class MissingRequiredColumnsError(PipelineError):
    pass


class DataValidationError(PipelineError):
    pass