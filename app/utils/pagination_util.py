def get_pagination_params(page: str = None, per_page: str = None, default_page: int = 1, default_per_page: int = 20):
  try:
    page_number = int(page) if page and int(page) > 0 else default_page
  except ValueError:
    page_number = default_page

  try:
    count = int(per_page) if per_page and int(per_page) > 0 else default_per_page
  except ValueError:
    count = default_per_page

  limit = count
  offset = (page_number - 1) * count

  return {
    "page": page_number,
    "per_page": count,
    "limit": limit,
    "offset": offset,
  }
