"""Project-specific exceptions with actionable failure messages."""


class RestaurantSalesError(Exception):
    """Base exception for this project."""


class InputFileNotFoundError(RestaurantSalesError):
    """Raised when a required input file is missing."""


class SchemaValidationError(RestaurantSalesError, ValueError):
    """Raised when required input columns are unavailable."""


class ProductMappingError(RestaurantSalesError, ValueError):
    """Raised when the product taxonomy file is missing or malformed."""


class OutputValidationError(RestaurantSalesError):
    """Raised when required pipeline artifacts fail validation."""
