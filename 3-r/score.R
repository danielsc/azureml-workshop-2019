#' Copyright(c) Microsoft Corporation.
#' Licensed under the MIT license.

library(jsonlite)

init <- function()
{
  model_path <- Sys.getenv("AZUREML_MODEL_DIR")
  model <- readRDS(file.path("model.rds"))
  message("model is loaded")
  
  function(data)
  {
    record <- as.data.frame(fromJSON(data))
    prediction <- predict(model, record)
    result <- as.character(prediction)
    toJSON(result)
  }
}
