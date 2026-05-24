
# use SimplePipeline for docx, pptx, xlsx, html, AsciiDoc, csv and md formats that don't heavily rely on complex visual formatting and images. 



import docling.document_converter
import time
import docling_core.types.doc.document
import docling.datamodel.base_models
import docling.datamodel.document
import logging
from src.code import paths
import typing

logger = logging.getLogger(__name__)


class DocPrepLineSimple:

    

    async def prepare_data(self) :
        try:
            
            logging.getLogger("docling").setLevel(logging.WARNING)


            # the source can be a local file path or an URL
            source_folder=paths.INPUT_DATA_DIR
            source_folder.mkdir(parents=True, exist_ok=True)
            input_file_path = source_folder / "FINAL FOOD DATASET" / "FOOD-DATA-GROUP1.csv"
           

          

             # for each document format, the document converter knows which format-specific backend to employ for parsing
            # the document and which pipeline to use for orchestrating the execution, along with any relevant options. 
            # While the document converter holds a default mapping, this configuration is parametrizable, so e.g. for the PDF format, different backends and different pipeline options can be used
            converter: docling.document_converter.DocumentConverter = docling.document_converter.DocumentConverter(
                allowed_formats=[
                    docling.datamodel.base_models.InputFormat.DOCX, 
                    docling.datamodel.base_models.InputFormat.HTML,
                    docling.datamodel.base_models.InputFormat.CSV,
                    docling.datamodel.base_models.InputFormat.XLSX,
                    docling.datamodel.base_models.InputFormat.PPTX,
                ],
            )

        
            # for each document format, the document converter knows which format-specific backend to employ for parsing
            # the document and which pipeline to use for orchestrating the execution, along with any relevant options. 
            # While the document converter holds a default mapping, this configuration is parametrizable, so e.g. for the PDF
            # format, different backends and different pipeline options can be used
            
            start_time=time.time()
            logger.info(f"Starting conversion of {input_file_path.name}")
            # convert multiple files at once
            #results: typing.Iterator [docling.datamodel.document.ConversionResult] = converter.convert_all([p])
            result: docling.datamodel.document.ConversionResult = converter.convert(source=input_file_path)
            pipeline_runtime= time.time() - start_time
            assert result.status== docling.datamodel.base_models.ConversionStatus.SUCCESS
            
            num_pages=len(result.pages)
            logger.info(f"Document converted in {pipeline_runtime:.2f} seconds.")
            logger.info(f" {num_pages / pipeline_runtime: .2f} pages/second.")

            doc: docling_core.types.doc.document.DoclingDocument = result.document
            transformed_doc=doc.export_to_markdown()
            
           

         
        except Exception as e:
            logger.error(f"Error in prepare_data: {str(e)}", exc_info=True)
