variable "credentials" {
  description = "My Credentials"
  default     = "../keys/datatalks-cred.json"
}

variable "project" {
  description = "Project"
  default     = "datatalks-ny-taxi"
}

variable "region" {
  description = "Region"
  default     = "europe-west1"
}

variable "zone" {
  description = "Zone"
  default     = "europe-west1-b"
}

variable "location" {
  description = "Project Location"
  default     = "EU"
}

variable "bq_dataset_name" {
  description = "Datatalks NY Taxi BigQuery dataset"
  default     = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = "Datatalks NY Taxi Storage Bucket Name"
  default     = "datatalks-ny-taxi-terra-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket storage class"
  default     = "STANDARD"
}