# use Pdf pipleline for pdf and scanned images

import os
from src.code import paths

# Set Hugging Face cache directory BEFORE importing docling
# This must be done before any imports that might use HuggingFace
# the hugging face models will be downloaded to the cache directory
hf_cache_dir = paths.HUGGINGFACE_MODELS_DIR
hf_cache_dir.mkdir(parents=True, exist_ok=True)
os.environ["HF_HOME"] = str(hf_cache_dir)


import docling.document_converter
import time
import docling.datamodel.accelerator_options
import docling_core.types.doc.document
import docling.datamodel.base_models
import docling.datamodel.pipeline_options
import docling.datamodel.document
import logging
import docling.pipeline.threaded_standard_pdf_pipeline
import typing

logger = logging.getLogger(__name__)


class DocPrepLineStandardPDF:

    

    async def prepare_data(self) :
        try:
            
            logging.getLogger("docling").setLevel(logging.WARNING)

             # the source can be a local file path or an URL
            source_folder=paths.INPUT_DATA_DIR
            source_folder.mkdir(parents=True, exist_ok=True)
            input_file_path = source_folder / "FINAL FOOD DATASET" / "FOOD-DATA-GROUP1.csv"

           

           # standard pdf pipeline without ocr
           # configure accelerator options for GPU
            accelerator_options=docling.datamodel.accelerator_options.AcceleratorOptions(
                device= docling.datamodel.accelerator_options.AcceleratorDevice.CUDA,  # or AcceleratorDevice.AUTO
            )

            pipeline_options= docling.datamodel.pipeline_options.ThreadedPdfPipelineOptions(
                accelerator_options=accelerator_options,
                ocr_batch_size=64,  # default 4
                layout_batch_size=64, # default 4
                table_batch_size= 4,  # currently not using GPU batching
            )
            pipeline_options.do_ocr= False


             # for each document format, the document converter knows which format-specific backend to employ for parsing
            # the document and which pipeline to use for orchestrating the execution, along with any relevant options. 
            # While the document converter holds a default mapping, this configuration is parametrizable, so e.g. for the PDF format, different backends and different pipeline options can be used
            converter: docling.document_converter.DocumentConverter = docling.document_converter.DocumentConverter(
            format_options={
                    docling.datamodel.base_models.InputFormat.PDF: docling.document_converter.PdfFormatOption(
                        pipeline_cls= docling.pipeline.threaded_standard_pdf_pipeline.ThreadedStandardPdfPipeline,
                        pipeline_options= pipeline_options
                    )
                }
            )

            start_time=time.time()
            converter.initialize_pipeline(docling.datamodel.base_models.InputFormat.PDF)
            init_runtime= time.time() - start_time
            logger.info(f"Pipeline initialized in {init_runtime:.2f} seconds")



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
            print(f"Error in prepare_data: {str(e)}")
            import traceback
            traceback.print_exc()
            return None


