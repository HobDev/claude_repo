# convert docs from differenct format. Splitting a pdf or using the page_range parameter in docling can split list, table or code block across page or chunk boundaries. Docling treats each part as a separate entity. Merging the resulting DoclingDocuments with DoclingDocument.concatenate() will not automatically heal or merge these split elements- they remain disjoint in the merged document. For example, a table split across two chunks will appear as two separate tables in the final document. Reliability and accuracy with the VLM backend depend on the specific model and prompt you use. 

# use vlm (vision language model) backend when you need to extract complex visual structures, tables, or image-based content, or when other backends fail to capture the document's structure.


import docling.document_converter
import docling.datamodel.accelerator_options
import docling.pipeline.vlm_pipeline
import docling.datamodel.base_models
import docling.datamodel.pipeline_options
import docling.datamodel.pipeline_options_vlm_model
import docling.datamodel.document
import docling.datamodel.settings
import docling_core.types.doc.document
from src.code import paths
import logging
import dotenv
import time
import os
import typing
import pathlib
from src.code import app_logs
import pydantic

_log= logging.getLogger(__name__)

dotenv.load_dotenv()


class DocPrepLineVLM:

    def __init__(self) -> None:
        """Initialize the Llama class."""
        self.VLLM_VLM_API_KEY: str = os.environ.get('VLLM_VLM_API_KEY') or ""
        self.VLLM_VLM_ENDPOINT: str = os.environ.get('VLLM_VLM_ENDPOINT') or ""
        self.VLM_MODEL: str = os.environ.get('VLM_MODEL') or ""
        self.batch_size=8

    async def prepare_data(self) :
        try:
            logging.getLogger("docling").setLevel(logging.WARNING)
            _log.setLevel(logging.INFO)

           # Make sure to set settings.perf.page_batch_size >= vlm_options.concurrency
            docling.datamodel.settings.settings.perf.page_batch_size= self.batch_size
            docling.datamodel.settings.settings.debug.profile_pipeline_timings=True
            
               # the source can be a local file path or an URL
            # source_folder=paths.INPUT_DATA_DIR
            # input_file_path = source_folder / "FINAL FOOD DATASET" / "FOOD-DATA-GROUP1.csv"

            input_file_path="https://arxiv.org/html/2408.09869v4"

            headers={"Authorization": f"Bearer {self.VLLM_VLM_API_KEY}"} if self.VLLM_VLM_API_KEY else {}


            vlm_options= docling.datamodel.pipeline_options_vlm_model.ApiVlmOptions(
                kind='api_model_options',
                url=pydantic.AnyUrl(self.VLLM_VLM_ENDPOINT),
                params=dict(
                    model=self.VLM_MODEL,
                    max_tokens=4096,  # reduced from models maximum context length(8000) to leave room for input tokens (image embeddings + prompt)
                    skip_special_tokens=False # needed for VLLM
                ),
                headers=headers,
                 # Make sure to set settings.perf.page_batch_size >= vlm_options.concurrency
                concurrency=8, 
                prompt="Convert this page to docling.",
                timeout=240,  # seconds
                scale=2.0,
                temperature=0.7,
                response_format= docling.datamodel.pipeline_options_vlm_model.ResponseFormat.MARKDOWN
            )

              # configure accelerator options for GPU
            accelerator_options=docling.datamodel.accelerator_options.AcceleratorOptions(
                device= docling.datamodel.accelerator_options.AcceleratorDevice.CUDA,  # or AcceleratorDevice.AUTO
            )

            pipeline_options= docling.datamodel.pipeline_options.VlmPipelineOptions(
                accelerator_options=accelerator_options,
                vlm_options=vlm_options,
                enable_remote_services=True
            )


            # for each document format, the document converter knows which format-specific backend to employ for parsing
            # the document and which pipeline to use for orchestrating the execution, along with any relevant options. 
            # While the document converter holds a default mapping, this configuration is parametrizable, so e.g. for the PDF
            # format, different backends and different pipeline options can be used
            converter: docling.document_converter.DocumentConverter = docling.document_converter.DocumentConverter(
                format_options={
                    docling.datamodel.base_models.InputFormat.PDF: docling.document_converter.PdfFormatOption(
                        pipeline_cls= docling.pipeline.vlm_pipeline.VlmPipeline,
                        pipeline_options= pipeline_options
                    )
                }
            )

            start_time=time.time()
            converter.initialize_pipeline(docling.datamodel.base_models.InputFormat.PDF)
            init_runtime= time.time() - start_time
            _log.info(f"Pipeline initialized in {init_runtime:.2f} seconds")



            # for each document format, the document converter knows which format-specific backend to employ for parsing
            # the document and which pipeline to use for orchestrating the execution, along with any relevant options. 
            # While the document converter holds a default mapping, this configuration is parametrizable, so e.g. for the PDF
            # format, different backends and different pipeline options can be used
            
            start_time=time.time()
            #app_logs.Logging.log_info(f"Starting conversion of {input_file_path.name}")
            # convert multiple files at once
            #results: typing.Iterator [docling.datamodel.document.ConversionResult] = converter.convert_all([p])
            result: docling.datamodel.document.ConversionResult = converter.convert(source=input_file_path)
            pipeline_runtime= time.time() - start_time
            assert result.status== docling.datamodel.base_models.ConversionStatus.SUCCESS
            
            num_pages=len(result.pages)
            _log.info(f"Document converted in {pipeline_runtime:.2f} seconds.")
            _log.info(f" {num_pages / pipeline_runtime: .2f} pages/second.")

            doc: docling_core.types.doc.document.DoclingDocument = result.document
            transformed_doc=doc.export_to_markdown()
            
            
                
        except Exception as e:
            app_logs.Logging.log_error(f"Error in prepare_data: {str(e)}")
            print(f"Error in prepare_data: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

