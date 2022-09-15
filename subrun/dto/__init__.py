from collections import namedtuple


Info = namedtuple("Info", ["process", "success", "return_code",
                           "output", "error", "timeout_expired"])


PipelineInfo = namedtuple("PipelineInfo", ["process", "success", "return_code",
                                           "output", "error", "return_codes",
                                           "timeout_expired"])
