
# import pandas as pd
# from typing import Annotated, Literal
# from datetime import datetime

# Reports = []
# report_final = ''
# def save_report(
#         name: Annotated[str, "Report name"],
#         content: Annotated[str, "Markdown content of report"],
#         ) -> str:
#     global Reports
#     r = {
#         'name': name,
#         'content': content,
#         'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         }
#     Reports.append(r)  # Use append() instead of +=
#     return f"Success: Report {name} saved."

# def get_info() -> str:
#     df_info = pd.DataFrame(Reports).sort_values(by='time')
#     info = '\n\n'.join(df_info['content'])
#     return info

# def save_report_final(
#         content: Annotated[str, "Markdown content of the full report"],
#         ) -> str:
#     global report_final
#     report_final = content
#     return f"Success: Final report is prepared and saved. TERMINATE"