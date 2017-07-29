"""
# nbconvert latex test
"""


"""
**Lorem ipsum** dolor sit amet, consectetur adipiscing elit. Nunc luctus bibendum felis dictum sodales. Ut suscipit, orci ut interdum imperdiet, purus ligula mollis *justo*, non malesuada nisl augue eget lorem. Donec bibendum, erat sit amet porttitor aliquam, urna lorem ornare libero, in vehicula diam diam ut ante. Nam non urna rhoncus, accumsan elit sit amet, mollis tellus. Vestibulum nec tellus metus. Vestibulum tempor, ligula et vehicula rhoncus, sapien turpis faucibus lorem, id dapibus turpis mauris ac orci. Sed volutpat vestibulum venenatis.
"""


"""
## Printed Using Python
"""


next_paragraph = """
Aenean vitae diam consectetur, tempus arcu quis, ultricies urna. Vivamus venenatis sem 
quis orci condimentum, sed feugiat dui porta.
"""

def nifty_print(text):
    """Used to test syntax highlighting"""
    
    print(text * 2)

nifty_print(next_paragraph)

"""
## Pyout
"""


Text = """
Aliquam blandit aliquet enim, eget scelerisque eros adipiscing quis. Nunc sed metus 
ut lorem condimentum condimentum nec id enim. Sed malesuada cursus hendrerit. Praesent 
et commodo justo. Interdum et malesuada fames ac ante ipsum primis in faucibus. 
Curabitur et magna ante. Proin luctus tellus sit amet egestas laoreet. Sed dapibus 
neque ac nulla mollis cursus. Fusce mollis egestas libero mattis facilisis.
"""
Text

"""
### Image
"""


from IPython.core.display import Image
Image(data="http://ipython.org/_static/IPy_header.png")
