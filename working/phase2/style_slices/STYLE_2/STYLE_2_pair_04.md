# STYLE_2 section pair 4

This file contains one or two `##` sections from docs/to_integrate/STYLE_2.md.

## ✅ Recommended Python 3.14 style-guide summary

Putting it all together for Python 3.14:

* Annotate all **public** module functions/methods with parameter and return types.
* Use classes (or `@dataclass`) for data-shapes.
* Use type aliases (`TypeAlias`), `Union`, `Literal`, etc., for unions/intersections.
* For simple local variables inside functions where the type is obvious, skip explicit annotations.
* Write forward-referencing hints naturally (no quotes) when possible.
* Avoid redundant annotations on simple locals.
* If your code inspects annotations at runtime, prefer `annotationlib.get_annotations()` rather than hacking `__annotations__`.

---

If you like, I can **generate a full Python 3.14 style-guide document** (with examples and dos/ don’ts) tailored from your original TypeScript-based guidance.

[1]: https://docs.python.org/3/whatsnew/3.14.html?utm_source=chatgpt.com "What's new in Python 3.14"
[2]: https://realpython.com/python-annotations/?utm_source=chatgpt.com "Python 3.14 Preview: Lazy Annotations"
[3]: https://www.nb-data.com/p/python-314-12-features-you-can-use?utm_source=chatgpt.com "Python 3.14: 12 Features You Can Use Today"
[4]: https://docs.python.org/3/howto/annotations.html?utm_source=chatgpt.com "Annotations Best Practices"
