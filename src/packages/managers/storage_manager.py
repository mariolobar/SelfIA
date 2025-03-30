"""
Provides AzureStorageManager class to manage the storage
"""

import json
from typing import Union, IO
from io import BytesIO
import logging
from datetime import datetime, timedelta
import pandas as pd
from azure.storage.blob import BlobServiceClient, BlobClient, generate_blob_sas, BlobSasPermissions
from src.packages.config.config import Config


class AzureStorageManager():
    """
    Manages Azure Blob Storage operations including uploading and checking blobs.
    
    Attributes
    ----------
    config : Config
        Configuration object containing Azure Storage settings.
    storage_account_name : str
        Azure Storage account name.
    sas_token : str
        Shared Access Signature token for Azure Storage access.
    storage_account_container : str
        Default container for the storage account.
    storage_path : str
        Path within the storage container.
    storage_account_key : str
        Key for the storage account.
    storage_account_cnn_str : str
        Connection string for the storage account.

    Methods
    -------
    upload_blob(container_name: str, blob: str, data: Union[bytes, IO[bytes]]) -> None
        Uploads a blob to Azure Blob Storage.
    check_blob(container_name: str, blob: str) -> bool
        Checks if a blob exists in Azure Blob Storage.
    """

    def __init__(self) -> None:
        """
        Initializes the AzureStorageManager instance by loading configuration settings.
        """
        # Load configuration
        self.config = Config()

        # Azure Storage Account
        self.storage_account_name = self.config.config_storage_account_name
        self.storage_account_url = f"https://{self.storage_account_name}.blob.core.windows.net"
        self.storage_account_container = self.config.config_storage_account_ip_container
        self.storage_account_key = self.config.config_storage_account_key
        self.storage_account_cnn_str = f"DefaultEndpointsProtocol=https;AccountName={self.storage_account_name};AccountKey={self.storage_account_key}"
        
    def get_blob_url_with_sas(self, container_name: str, blob_filename: str) -> str:
        """
        Generates a SAS URL with read permissions for a specific blob in a container.

        Parameters
        ----------
        container_name : str
            The name of the Azure storage container.
        blob_filename : str
            The name of the blob file to generate the URL for.

        Returns
        -------
        str
            A URL with SAS token for accessing the blob.
        
        Raises
        ------
        ValueError
            If storage account name or key is not set in the configuration.
        """
        if not self.storage_account_name or not self.storage_account_key:
            raise ValueError("Azure Storage account name or key is not set in environment variables.")
        
        # Generate SAS token
        sas_token = generate_blob_sas(
            account_name=self.storage_account_name,
            container_name=container_name,
            blob_name=blob_filename,
            account_key=self.storage_account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(hours=1)
        )
        
        # Construct full URL with SAS token
        blob_url_with_sas = f"https://{self.storage_account_name}.blob.core.windows.net/{container_name}/{blob_filename}?{sas_token}"
        return blob_url_with_sas
    
    def upload_blob(self, container_name: str, blob: str, data: Union[bytes, IO[bytes]], metadata=None) -> None:
        """
        Uploads a blob to the specified container in Azure Blob Storage.

        Parameters
        ----------
        container_name : str
            The name of the Azure storage container.
        blob : str
            The name of the blob within the container.
        data : Union[bytes, IO[bytes]]
            The data to upload, either as a bytes object or as a file-like object opened in
            binary mode.

        Returns
        -------
        None

        Notes
        -----
        This method overwrites the blob if it already exists in the container.
        """
        # Get BlobClient
        blob = BlobClient.from_connection_string(
            conn_str=self.storage_account_cnn_str,
            container_name=container_name,
            blob_name=blob
        )
        # Upload blob
        blob.upload_blob(
            data=data,
            overwrite=True
        )

        # Set metadata if provided
        if metadata:
            blob.set_blob_metadata(metadata)

    def check_blob(self, container_name: str, blob: str) -> bool:
        """
        Checks if a blob exists in the specified container in Azure Blob Storage.

        Parameters
        ----------
        container_name : str
            The name of the Azure storage container.
        blob : str
            The name of the blob to check.

        Returns
        -------
        bool
            True if the blob exists, False otherwise.
        """
        # Get BlobSeviceClient
        blob_service_client = BlobServiceClient.from_connection_string(
            conn_str=self.storage_account_cnn_str,
        )
        # Get blob client
        blob_client = blob_service_client.get_blob_client(
            container=container_name, blob=blob
        )

        return blob_client.exists()

    def get_blob(self, container_name: str, blob: str, fmt: str):
        """
        Downloads and returns the content of a blob from Azure Blob Storage in the specified format.

        Parameters
        ----------
        container_name : str
            The name of the Azure storage container.
        blob : str
            The name of the blob to be downloaded.
        format : str
            The desired format of the downloaded content. Options are 'json', 
            'pdf', 'csv', 'txt', 'excel', 'img'.

        Returns
        -------
        Any
            The content of the blob in the specified format:
            - For 'json': Returns the content as a JSON object (dict).
            - For 'pdf': Returns a PyMuPDF document object.
            - For 'csv': Returns a pandas DataFrame.
            - For 'txt': Returns the content as a string.
            - For 'xlsx': Returns the content as a BytesIO object.
            - For 'img': Returns the content as bytes.

        Raises
        ------
        ValueError
            If an invalid format is specified.
        """

        blob_service_client = BlobServiceClient.from_connection_string(
            conn_str=self.storage_account_cnn_str,
        )

        blob_client = blob_service_client.get_blob_client(
            container=container_name, blob=blob
        )
        stream = blob_client.download_blob()
        result = stream.readall()

        if fmt == "json":
            data = json.loads(result)
        elif fmt == "pdf":
            pdf_stream = BytesIO(result)
            return pdf_stream
        elif fmt == "csv":
            data = pd.read_csv(BytesIO(result))
        elif fmt == "txt":
            data = result.decode("utf-8")
        elif fmt == "xlsx":
            data = BytesIO(result)
            return data
        elif fmt == 'img':
            data = BytesIO(result)
            return data 
        elif fmt == 'docx':
            data = BytesIO(result)
            return data
        else:
            raise ValueError("Specify a valid format to read data: [json, csv, txt, excel]")
        return data
    
    def list_blobs(self, container_name: str):
        """
        Lists all blobs in the specified Azure Blob Storage container.

        Parameters
        ----------
        container_name : str
            The name of the Azure storage container from which to list blobs.

        Returns
        -------
        List[str]
            A list of blob names present in the specified container.
        
        Raises
        ------
        Exception
            If the container does not exist or if there is an issue with the connection.
        """

        blob_service_client = BlobServiceClient.from_connection_string(
            conn_str=self.storage_account_cnn_str,
        )
         
        container_client = blob_service_client.get_container_client(container_name)

        blob_list = container_client.list_blobs()

        blobs = [blob.name for blob in blob_list]

        return blobs
    
    def list_blobs_with_metadata(self, container_name: str):
        blob_service_client = BlobServiceClient.from_connection_string(
            conn_str=self.storage_account_cnn_str,
        )

        container_client = blob_service_client.get_container_client(container_name)

        blob_list = container_client.list_blobs()
        blobs_with_metadata = []

        for blob in blob_list:

            blob_client = container_client.get_blob_client(blob.name)

            properties = blob_client.get_blob_properties()
            
            blobs_with_metadata.append({
                "id": blob.name,
                "name": properties.metadata.get("file_name")
            })

        return blobs_with_metadata
