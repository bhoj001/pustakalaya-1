#  document/models.py
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

from pustakalaya_apps.collection.models import Collection
from pustakalaya_apps.core.abstract_models import (
    AbstractItem,
    AbstractSeries,
    AbstractTimeStampModel,
    LinkInfo
)
from pustakalaya_apps.core.models import (
    Publisher,
    Biography,
    Keyword,
    Sponsor,
    EducationLevel,
    Language
)
from .search import DocumentDoc


def __file_upload_path(instance, filepath):
    # Should return itemtype/year/month/filename
    # return instance.type
    # return document/pdf/year/month/filename
    pass


class Document(AbstractItem):
    """Book document type to store book type item
    Child class of AbstractItem
    """

    ITEM_INTERACTIVE_TYPE = (
        ("yes", _("Yes")),
        ("no", _("No")),
        ("NA", _("Not applicable")),
    )

    DOCUMENT_TYPE = (
        ("book", _("Book")),
        ("working paper", _("Working paper")),
        ("thesis", _("Thesis")),
        ("journal paper", _("Journal paper")),
        ("technical report", _("Technical report")),
        ("article", _("Article")),

    )

    DOCUMENT_FILE_TYPE = (
        ("ppt", _("PPT")),
        ("doc", _("Doc")),
        ("docx", _("Docx")),
        ("pdf", _("PDF")),
        ("pdf", _("PDF")),
        ("xlsx", _("Excel")),
        ("epub", _("Epub")),
        ("rtf", _("Rtf")),
        ("mobi", _("Mobi")),
    )

    collections = models.ManyToManyField(
        Collection,
        verbose_name=_("Add to these collections"),
    )

    document_type = models.CharField(
        _("Document type"),
        max_length=40,  # TODO: Change to match the exact value.
        choices=DOCUMENT_TYPE
    )

    document_file_type = models.CharField(
        _("Document file type"),
        choices=DOCUMENT_FILE_TYPE,
        max_length=23
    )

    document_series = models.ForeignKey(
        "DocumentSeries",
        verbose_name=_("Series"),
        on_delete=models.CASCADE
    )

    education_levels = models.ManyToManyField(
        EducationLevel,
        verbose_name=_("Education Levels"),
        blank=True
    )

    languages = models.ManyToManyField(
        Language,
        verbose_name=_("Language(s)")
    )

    document_interactivity = models.CharField(
        verbose_name=_("Interactive"),
        max_length=15,
        choices=ITEM_INTERACTIVE_TYPE
    )

    # This field should be same on all other model to make searching easy in search engine.
    type = models.CharField(
        max_length=255, editable=False, default="document"
    )

    # document_category = models.ForeignKey(
    #     Category,
    #     on_delete=models.CASCADE,
    #     verbose_name=_("Document Category")
    # )

    document_total_page = models.PositiveIntegerField(
        verbose_name=_("Total Pages"),
        blank=True,
    )

    document_authors = models.ManyToManyField(
        Biography,
        verbose_name=_("Author(s)"),
        related_name="authors",
        blank=True,
    )

    document_editors = models.ManyToManyField(
        Biography,
        verbose_name=_("Editor(s)"),
        related_name="editors",
        blank=True,
    )

    document_illustrators = models.ManyToManyField(
        Biography,
        verbose_name=_("Document Illustrator"),
        related_name="illustrators",
        blank=True
    )

    publisher = models.ForeignKey(
        Publisher,
        verbose_name=_("Publisher name")
    )
    # Better to have plural name
    keywords = models.ManyToManyField(
        Keyword,
        verbose_name=_("Select list of keywords")
    )

    document_thumbnail = models.ImageField(
        upload_to="uploads/thumbnails/audio/%Y/%m/%d",
        max_length=255
    )

    sponsors = models.ManyToManyField(
        Sponsor,
        verbose_name=_("Sponsor"),
        blank=True,

    )

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title

    def doc(self):
        """Create and return document object"""
        obj = DocumentDoc(
            meta={'id': self.id},
            id=self.id,
            title=self.title,
            abstract=self.abstract,
            type=self.type,
            education_level=[education_level.level for education_level in self.education_levels.all()],
            communities= [collection.community_name for collection in self.collections.all()],
            collections = [collection.collection_name for collection in self.collections.all()],
            language= [language.language for language in self.languages.all()],
            license_type=self.license_type,
            year_of_available=self.year_of_available,
            publication_year=self.publication_year,
            place_of_publication=self.place_of_publication,
            created_date=self.created_date,
            updated_date=self.updated_date,

            # Common fields in document, audio and video library
            publisher=self.publisher.publisher_name,
            sponsors=[sponsor.name for sponsor in self.sponsors.all()],  # Multi value # TODO some generators
            keywords=[keyword.keyword for keyword in self.keywords.all()],

            # Document type specific
            document_thumbnail=self.document_thumbnail.name,
            # document_identifier_type=self.document_identifier_type,
            document_file_type=self.document_file_type,
            document_interactivity=self.document_interactivity,
            document_type=self.document_type,
            document_authors=[
                author.getname for author in self.document_authors.all()
                ],
            document_illustrators=[
                illustrator.getname for illustrator in self.document_illustrators.all()
                ],  # Multi value TODO generator
            document_editors=[
                editor.getname for editor in self.document_editors.all()
                ]  # Multi value

        )

        return obj

    def index(self):
        """index or update a document instance to elastic search index server"""
        self.doc().save()
        return self.doc().to_dict(include_meta=True)

    def delete_index(self):
        self.doc().delete()

    def get_absolute_url(self):
        pass


class DocumentSeries(AbstractSeries):
    """BookSeries table inherited from AbstractSeries"""

    def __str__(self):
        return self.series_name


class DocumentFileUpload(AbstractTimeStampModel):
    """Class to upload the multiple document objects"""

    file_name = models.CharField(
        _("File name"),
        max_length=255,
    )

    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE
    )

    upload = models.FileField(
        upload_to="uploads/documents/%Y/%m/",
        max_length=255
    )

    def __str__(self):
        return self.file_name


class DocumentLinkInfo(LinkInfo):
    document = models.ForeignKey(
        Document,
        verbose_name=_("Link"),
        on_delete=models.CASCADE,

    )

    def __str__(self):
        return self.document.title


class DocumentIdentifier(AbstractTimeStampModel):
    identifier_type = models.CharField(
        verbose_name=_("Identifier Type"),
        max_length=8,
        choices=(
            ("issn", _("ISSN")),
            ("ismn", _("ISMN")),
            ("govt_doc", _("Gov't Doc")),
            ("uri", _("URI")),
            ("isbn", _("ISBN"))
        )
    )
    identifier_id = models.CharField(
        _("Identifier ID"),
        blank=True,
        max_length=10
    )

    document = models.OneToOneField(
        Document,
        verbose_name=_("document"),
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.identifier_type
