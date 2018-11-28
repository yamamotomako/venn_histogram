create table Gene(
    serialno text,
    GeneName text,
    GeneSummary text,
    Chromosome text,
    PrimaryTranscript text,
    Position text,
    GeneAnnotation text,
    Variant text,
    VariantId text,
    VariantType text,
    ChromosomeLocationChange text,
    AminoAcid text,
    DNACoding text,
    Classification text,
    ClassificationSource text,
    Effect text,
    InputValue text,
    TranscriptId text,
    AlleleFrequency text,
    SequencingDepth text,
    AnnotationText text,
    OtherDatabaseIds text
);
create index id_gene on Gene(serialno);



create table SampleInfo(
    serialno text,
    UserId text,
    AnalysisDate text,
    Version text,
    ConditionId text,
    ConditionName text,
    Age text,
    Gender text,
    Folder text,
    Files text,
    CaseId text,
    CaseName text,
    SampleName text
);
create index id_si on SampleInfo(serialno);


create table Drug(
    serialno text,
    DrugName text,
    HighestEvidenceLevel text,
    Category text,
    ApprovalStatus text,
    MOA text
);
create index id_drug on Drug(serialno);


create table ClinicalTrials(
    serialno text,
    NCTId text,
    Title text,
    Phase text,
    RecruitingStatus text,
    CountryList text
);
create index id_ct on ClinicalTrials(serialno);



create table GeneDrugEvidenceLevels(
    serialno text,
    GeneName text,
    IV_TrialPhase text,
    IV_SameCancerDrugs text,
    IV_EvidenceLevel text,
    IV_Evidences text,
    IV_EvidencesSummary text,
    AS_OtherCancerDrugs text,
    AS_EvidenceLevel text,
    AS_Evidences text,
    AS_EvidencesSummary text,
    AO_OtherCancerDrugs text,
    AO_EvidenceLevel text,
    AO_Evidences text,
    AO_EvidencesSummary text
);
create index id_gdel on GeneDrugEvidenceLevels(serialno);


create table DrugAssociations(
    serialno text,
    GeneName text,
    Pathway text
);
create index id_da on DrugAssociations(serialno);


