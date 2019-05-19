from django.db import models


class LawABC(models.Model):
    case = models.CharField(max_length=100)
    url = models.URLField(max_length=100, blank=True)

    class Meta:
        abstract = True

# class BodyABC(models.Model):
#     title = models.CharField(max_length=100, blank=True)
#     body_text = models.CharField(max_length=3750)
#
#     class Meta:
#         abstract = True


class FedStatute(LawABC):
    case_law_id = models.CharField(max_length=10)

    def save(self, *args, **kwargs):
        self.case_law_id = "#{}".format(self.id)
        super(FedStatute, self).save(*args, **kwargs)

    def __str__(self):
        return self.case

    class Meta:
        db_table = "federal_statutes"


class ReportCase(LawABC):
    plaintiff = models.CharField(max_length=50)
    defendant = models.CharField(max_length=50)
    tried = models.BooleanField(default=False)
    # charge = models.ForeignKey(
    #         Charge,
    #         related_name="charge",
    #         related_query_name="charges",
    #         on_delete=models.CASCADE)
    counts = models.PositiveSmallIntegerField(default=1)
    court = models.CharField(max_length=50)
    num_convictions = models.PositiveSmallIntegerField(default=0)
    num_not_guilty = models.PositiveSmallIntegerField(default=0)
    hung_jury = models.PositiveSmallIntegerField(default=0)
    ptid = models.CharField(max_length=10)

    def save(self, *args, **kwargs):
        self.ptid = "#{}".format(self.id)
        super(ReportCase, self).save(*args, **kwargs)

    def __str__(self):
        return "{plaintiff} vs {defendant}".format(
                plaintiff=self.plaintiff,
                defendant=self.defendant)

    class Meta(LawABC.Meta):
        db_table = "report_cases"


class Charge(models.Model):
    case = models.ForeignKey(
            ReportCase,
            on_delete=models.CASCADE,
            verbose_name="investigation case",
            related_query_name="report_cases",
            related_name="report_case"
            )
    federal_charge = models.CharField(max_length=100)

    class Meta:
        db_table = "charges"

    def __str__(self):
        return self.federal_charge


class Footnote(models.Model):
    VOLUME1 = "VOL1"
    VOLUME2 = "VOL2"
    QUESTIONS = "QUES"

    SECTION = [
            (VOLUME1, "Volume I"),
            (VOLUME2, "Volume 2"),
            (QUESTIONS, "Questions"),
            ]

    # report = models.ForeignKey(
    #         Report,
    #         on_delete=models.CASCADE,
    #         related_name="section",
    #         related_query_name="sections")
    section = models.CharField(max_length=4, choices=SECTION)
    footnote_number = models.PositiveSmallIntegerField()
    text = models.TextField(max_length=2000)
    listid = models.CharField(max_length=10)
    page_number = models.PositiveSmallIntegerField(blank=True)

    def save(self, *args, **kwargs):
        self.listid = "#{}" + str(self.footnote_number)
        super(Footnote, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.footnote_number)

    class Meta:
        db_table = "footnotes"


class Report(models.Model):
    VOLUME_I = "VI"
    VOLUME_II = "VII"
    APPENDIX_A = "APA"
    APPENDIX_B = "APB"
    APPENDIX_C = "APC"
    APPENDIX_D = "APD"

    PART_OF_REPORT = [
            (VOLUME_I, "Volume I"),
            (VOLUME_II, "Volume II"),
            (APPENDIX_A, "Appendix A"),
            (APPENDIX_B, "Appendix B"),
            (APPENDIX_C, "Appendix C"),
            (APPENDIX_D, "Appendix D"),
            ]

    INTRO = "IN"
    EXECUTIVE = "EX"
    SECTION = "SE"
    CONCLUSION = "C"

    REPORT_CHOICES = [
            (INTRO, "Into"),
            (EXECUTIVE, "Executive Summary"),
            (SECTION, "Section"),
            (CONCLUSION, "Conclusion"),
            ]

    MAIN = "M"
    SUB_SECTION_1 = "S1"
    SUB_SECTION_2 = "S2"
    SUB_SECTION_3 = "S3"
    SUB_SECTION_4 = "S4"

    REPORT_SUBSECTION = [
            (MAIN, "Main"),
            (SUB_SECTION_1, "Subsection 1"),
            (SUB_SECTION_2, "Sub Section 2"),
            (SUB_SECTION_3, "Sub Section 3"),
            (SUB_SECTION_4, "Sub Section 4"),
            ]

    part_of_report = models.CharField(
            max_length=3,
            choices=PART_OF_REPORT,
            default=VOLUME_I,
            help_text="Highest level of the report",)
    section_of_report = models.CharField(
            max_length=2,
            choices=REPORT_CHOICES,
            default=SECTION,
            help_text="Where in the report")
    sub_section_of_report = models.CharField(
            max_length=2,
            choices=REPORT_SUBSECTION,
            default=MAIN,
            help_text="What level in the report. This is used for the ol type")
    section_title = models.CharField(
            max_length=100,
            help_text="This is what is bold at beginning of the section."
            )
    # body = models.ForeignKey(
    #         Body,
    #         on_delete=models.CASCADE,
    #         related_query_name="bodies",
    #         related_name="body")
    # footnote = models.ForeignKey(
    #         Footnote,
    #         on_delete=models.CASCADE,
    #         related_name="footnote",
    #         related_query_name="footnotes"
    #         )
    page_number = models.PositiveSmallIntegerField(help_text="This is the actual page in the report")
    adobe_page = models.PositiveSmallIntegerField(blank=True, help_text="What is the adobe page?")
    slug = models.SlugField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "report"

    def __str__(self):
        return "Part {part} of {sec} of {sub} with title: {title}".format(
                part=self.part_of_report,
                sec=self.section_of_report,
                sub=self.sub_section_of_report,
                title=self.section_title)


class Body(models.Model):
    report = models.ForeignKey(
            Report,
            on_delete=models.CASCADE,
            verbose_name="the related section of the report",
            related_name="report",
            related_query_name="reports",

            )
    title = models.CharField(
            max_length=100,
            blank=True,
            help_text="What is the title for this section of text.")
    text = models.TextField(
            help_text="Only enter a paragraph at a time."
            )

    # body_id = models.ForeignKey(
    #         "self",
    #         on_delete=models.CASCADE,
    #         related_query_name="body_id",
    #         related_name="bodies_ids")

    class Meta:
        db_table = "body"

    def __str__(self):
        return str(self.title)

# class Report(models.Model):
#     section = models.ForeignKey(
#             Section,
#             on_delete=models.CASCADE,
#             related_query_name="sections",
#             related_name="section"
#             )
#     page_number = models.PositiveSmallIntegerField()
#     adobe_page = models.PositiveSmallIntegerField()
#
#     class Meta:
#         db_table = "report"
#
#     def __str__(self):
#         return self.section.section.__str__()


class Glossary(models.Model):
    ABBREVIATIONS = [
            ("N", "Name"),
            ("E", "Entity"),
            ("A", "Acronym"),
            ]

    abbrev = models.CharField(max_length=1, choices=ABBREVIATIONS)
    text = models.TextField()
    glossaryid = models.CharField(
            max_length=10,
            help_text="This is used in the template id field"
            )

    def save(self, *args, **kwargs):
        self.glossaryid = "#{g}".format(g=self.id)

    class Meta:
        db_table = "glossary"

    def __str__(self):
        return self.abbrev


class Question(models.Model):

    INTRODUCTION = "INT"
    PART_I = "I"
    PART_II = "II"
    PART_III = "III"
    PART_IV = "IV"
    PART_V = "V"

    PART = [
            (INTRODUCTION, "Introduction"),
            (PART_I, "I"),
            (PART_II, "II"),
            (PART_III, "III"),
            (PART_IV, "IV"),
            (PART_V, "V"),
            ]

    INTRO = "INTRO"
    QUESTION = "QUES"
    SUB_QUESTION = "SUBQ"
    LEVELII = "LEV2"

    CATEGORY = [
            (INTRO, "Introduction"),
            (QUESTION, "Question"),
            (SUB_QUESTION, "Level 1"),
            (LEVELII, "Level 2"),
            ]
    part = models.CharField(max_length=3, choices=PART, default=PART_I)
    category = models.CharField(max_length=5, choices=CATEGORY, default=QUESTION)
    title = models.CharField(
            max_length=100,
            help_text="Explanation Of the Question",
            blank=True
            )

    # footnote = models.ForeignKey(
    #         Footnote,
    #         on_delete=models.CASCADE,
    #         related_name="question_footnote",
    #         related_query_name="question_footnotes")

    class Meta:
        db_table = "questions"

    def __str__(self):
        return self.title

# class Answer(models.Model):
#     question = models.ForeignKey(
#             Question,
#             on_delete=models.CASCADE,
#             related_query_name="questions",
#             related_name="question"
#             )
#     answer = models.TextField()
#
#     class Meta:
#         db_table = "answers"
#
#     def __str__(self):
#         return self.question.title


class QAText(models.Model):

    INTRODUCTION = "I"
    QUESTION = "Q"
    SUB_QUESTION = "S"
    ANSWER = "A"
    LEVEL2 = "2"
    Q_OR_A = [
            (INTRODUCTION, "Introduction"),
            (QUESTION, "Question"),
            (SUB_QUESTION, "Level 1"),
            (LEVEL2, "Level II"),
            (ANSWER, "Answer"),
            ]
    qa_choice = models.CharField(max_length=1, choices=Q_OR_A)
    question = models.ForeignKey(
            Question,
            on_delete=models.CASCADE,
            verbose_name="question being asked",
            related_query_name="questions",
            related_name="question"
            )
    text = models.TextField()

    class Meta:
        db_table = "qa_text"

    def __str__(self):
        return self.qa_choice

# TODO Clean up commented fields in models
# TODO Create docstring in all Models
# TODO Add page number to Either QAText or Question Model.
# TODO Should  There be a "title" text field to QA Text?
