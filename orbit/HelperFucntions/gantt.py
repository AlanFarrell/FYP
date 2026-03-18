import plotly.express as px
import pandas as pd

def gantt(timeWindows):
    df = pd.DataFrame(timeWindows, columns=["Start", "End"])
    df["Task"] = "Coverage"

    fig = px.timeline(df, x_start = "Start", x_end = "End", y = "Task", color_discrete_sequence=["#4C6EF5"])
    fig.update_yaxes(autorange="reversed", title = "")


    if not df.empty:
        xmin, xmax = df["Start"].min(), df["End"].max()
        fig.update_xaxes(
            range=[xmin, xmax],
            tickformat="%H:%M",
            showgrid=True, gridcolor="rgba(0,0,0,0.1)"
        )

    fig.update_layout(
        height=260,
        showlegend=False,
        margin=dict(l=40, r=20, t=40, b=40),
        xaxis_title="Time (UTC)",
        plot_bgcolor="rgba(245,248,255,1)"
    )





    fig.show()