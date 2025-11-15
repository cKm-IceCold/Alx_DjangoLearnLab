
---

### `delete.md`
```markdown
# Delete Operation

```python
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
Book.objects.all()
# Output: <QuerySet []>
