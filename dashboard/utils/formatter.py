def format_number(num):
    """
    Convert numbers into K, M, B format.
    """

    num = float(num)

    if num >= 1_000_000_000:
        return f"{num/1_000_000_000:.1f}B"

    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"

    if num >= 1_000:
        return f"{num/1_000:.1f}K"

    return str(int(num))