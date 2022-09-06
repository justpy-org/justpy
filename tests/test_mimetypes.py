"""
Created on 2022-08-31
@author: wf
"""
from tests.basetest import Basetest
from mimetypes import guess_type
from starlette.responses import FileResponse


class TestMimetypes(Basetest):
    """
    test the mimetype handling
    """

    def testMimeTypes(self):
        """
        test the mimetypes
        """
        examples = [
            (
                "js",
                ["text/javascript", "application/javascript"],
            ),  # https://stackoverflow.com/questions/21098865/text-javascript-vs-application-javascript
            ("html", ["text/html"]),
            ("css", ["text/css"]),
            ("svg", ["image/svg+xml"]),
        ]
        for ext, expected in examples:
            filename = f"somefile.{ext}"
            mtype, _strictness = guess_type(filename)
            smtype = FileResponse(filename).media_type
            print(f"{ext}:{mtype}:{smtype}")
            self.assertIn(mtype, expected)
            self.assertIn(smtype, expected)
