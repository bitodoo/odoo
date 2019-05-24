# Example
## In view:
```html
   <button name="print_late_comming" class="oe_highlight" string="Late comming PDF" type="object"/>
   <button name="print_late_comming_xls" class="oe_highlight" string="Late comming XLS" type="object"/>
```
## In python:
```python
  import xlsxwriter
  from io import BytesIO
  from odoo.modules.module import get_module_resource
  . 
  .
  .
  def pdf_file(self):
      pdf_path = get_module_resource('bo_btn_download_file', 'files', 'pdf_file.pdf')
      return open(pdf_path, 'rb').read()

  def print_late_comming(self):
      self.ensure_one()
      return self.env['ir.actions.act_url'].binary_content(model=self._name,
                                                           method='pdf_file',
                                                           id=self.id,
                                                           filename='pdf_file.pdf',
                                                           mimetype='application/pdf')

  def xls_file(self):
      output = BytesIO()
      wb = xlsxwriter.Workbook(output, {
            'default_date_format': 'dd/mm/yyyy'
        })
      sheet = wb.add_worksheet('Stock Card')

      sheet.write(0, 0, "Company:", wb.add_format({'bold': True}))
      wb.close()
      output.seek(0)
      return output.read()

  def print_late_comming_xls(self):
      self.ensure_one()
      return self.env['ir.actions.act_url'].binary_content(model=self._name,
                                                             method='xls_file',
                                                             id=self.id,
                                                             filename='xls_file.xls',
                                                             mimetype='application/octet-stream')
```
Resume
## Model
```python
ir.actions.act_url
```

## Method
```python
binary_content(model=self._name,
                   method='xls_file',
                   id=self.id,
                   filename='xls_file.xls',
                   mimetype='application/octet-stream')
```

## Params
All params required
- **model**: Model name
- **method**: Method return out binary
- **id**: Id record
- **filename**: Name & extension file
- **mimetype**: Mimetype