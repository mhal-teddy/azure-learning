import azure.functions as func
import datetime
import json
import logging

app = func.FunctionApp()

@app.route(route="test", auth_level=func.AuthLevel.FUNCTION)
@app.sql_input(
    arg_name="salesOrder",
    command_text="SELECT TOP 10 [ProductID], [UnitPrice] [ModifiedDate] FROM SalesLT.SalesOrderDetail",
    command_type="Text",
    connection_string_setting="SqlConnectionString",
)
def test(req: func.HttpRequest, salesOrder: func.SqlRowList) -> func.HttpResponse:
    rows = list(map(lambda r: json.loads(r.to_json()), salesOrder))

    return func.HttpResponse(
        json.dumps(rows),
        status_code=200,
        mimetype="application/json",
    )