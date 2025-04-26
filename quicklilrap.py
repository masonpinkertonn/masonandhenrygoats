import textwrap

wrapper = textwrap.TextWrapper(width=4)

lst = wrapper.wrap(text="wassupmyn")

print(lst)