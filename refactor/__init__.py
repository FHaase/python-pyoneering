def load_module(current_version, stages=None, skip_validation=False, preset=None):
    from refactor.deprecator import Deprecator

    module = Deprecator(current_version, stages=stages, skip_validation=skip_validation, preset=preset)
    return module.deprecated, module.refactored
