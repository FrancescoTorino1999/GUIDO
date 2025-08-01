import enum


class CadocsIntents(enum.Enum):
    GetSmells = "get_smells"
    GetSmellsDate = "get_smells_date"
    Report = "report"
    Info = "info"
    Geodispersion = "geodispersion"
    CommunityInspectorAnalyze = "community_inspector_analyze"
    CommunityInspectorResults = "community_inspector_results"
