## Overview
A Remote Code Execution (RCE) vulnerability exists in the DICOM file import procedure in Invesalius3.

This vulnerability afflicts all versions from 3.1.99991 to 3.1.99998.

The exploitation steps of this vulnerability involve the use of a crafted DICOM file which, once imported inside the victim's client application allows an attacker to gain remote code execution over the victim's machine.

----

## Detailed description

Invesalius3 versions from 3.1.99991 to 3.1.99998 (latest available at the time of writing) contain the following vulnerable function inside the `invesalius/reader/dicom.py` script file.

```python
430    def GetImagePosition(self):
431     """
432     Return [x, y, z] (number list) related to coordinates
433     of the upper left corner voxel (first voxel transmitted).
434     This value is given in mm. Number might be floating point
435     or integer.
436     Return "" if field is not defined.
437
438     DICOM standard tag (0x0020, 0x0032) was used.
439     """
440     try:
441         data = self.data_image[str(0x020)][str(0x032)].replace(",", ".")
442     except KeyError:
443         return ""
444     if data:
445        return [eval(value) for value in data.split("\\")]
446        return ""
```

This function is triggered whenever a new DICOM file is imported.

In particular, the position of the imported image is calculated based on the coordinates contained in the image's position indexes in the tag at position `(0x020, 0x032)`.

The coordinates' values are separated from `\` characters. An example is the following: `5.1\4.3\3.2`.

Since the eval function is called for each value inside that range, where each value is taken by removing the `\` characters, an attacker might inject a malicious python payload after the last coordinate value (preceded by a `\` character) in order to cause the python code to be executed by the eval function.

Also notice that the payload cannot contain `,` characters, since they are replaced from the payload with `.`, as `line 441` suggests.

