from pydantic import BaseModel, Field


class WeatherResponse(BaseModel):
    city: str = Field(description="Name of the city")
    temperature: float = Field(description="Temperature in Celsius")
    condition: str = Field(description="Current weather condition")