# Load the ggplot2 package which provides
# the 'mpg' dataset.
library(ggplot2)
library(shiny)
library(azuremlsdk)
library(jsonlite)
library(data.table)

ws <- load_workspace_from_config()
all_data <- fread('../data/IBM-Employee-Attrition.csv',stringsAsFactors = TRUE)
# remove useless fields 
all_data = within(all_data, rm(EmployeeCount, Over18, StandardHours, EmployeeNumber))
# make sure attrition is a factor
for (col in c('Attrition')) 
  set(all_data, j=col, value=as.factor(all_data[[col]]))

# Get service from the workspace to refresh the object
service <- get_webservice(ws, name = 'attritionr')


# Define UI for slider demo app ----
ui <- fluidPage(
  titlePanel("Score AzureML Model"),
  
  # Create a new row for the table.
  DT::dataTableOutput("table"),
  h4("JSON sent to service"),
  verbatimTextOutput("json"),
  h4("Result returned by service"),
  verbatimTextOutput('result')
)

# Define server logic for slider examples ----
server <- function(input, output) {
  
  # Filter data based on selections
  output$table <- DT::renderDataTable(all_data,
                                      selection = 'single')
  
  output$json <- renderText({
    if (is.null(input$table_rows_selected)) {
      "select a table row"
    } else {
      sample = all_data[input$table_rows_selected]
      sample$Attrition = NULL
      toJSON(sample)
    }
  })
  
  output$result <- renderText({
    if (is.null(input$table_rows_selected)) {
      "select a table row"
    } else {
      sample = all_data[input$table_rows_selected]
      sample$Attrition = NULL
      result = invoke_webservice(service, toJSON(sample))
      result
    }
  })
  
  
}

# Create Shiny app ----
shinyApp(ui, server)




