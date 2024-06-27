from pydantic import BaseModel

class SummaryModel(BaseModel):
    summary_text_en: str
    summary_text_fr: str
    summary_text_es: str
    summary_text_de: str
    summary_text_it: str
