from contextvars import ContextVar

import structlog

correlation_id: ContextVar[str] = ContextVar("correlation_id", default="")


def add_correlation(logger, method_name, event_dict):
    event_dict["correlation_id"] = correlation_id.get()
    return event_dict


def setup_logging():
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            add_correlation,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer()
            if __debug__
            else structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(20),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )
