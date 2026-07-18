from datetime import date
from pydantic import BaseModel, Field
from typing_extensions import TypedDict


class RawTrendResultsWithNaverBlog(BaseModel):
    """A raw result of trend search with naver blog"""

    title: str = Field(description="The title of the blog")
    link: str = Field(description="The link of the blog")
    description: str = Field(description="The description of the blog")
    bloggername: str = Field(description="The name of the blogger")
    bloggerlink: str = Field(description="The link of the blogger's homepage")
    postdate: str = Field(description="The date the blog was posted")


class Result(BaseModel):
    """A result of blog"""

    title: str = Field(description="The title of the blog")
    link: str = Field(description="The link of the blog")
    description: str = Field(description="The blog's rating out of 10")
    postdate: str = Field(description="The date the blog was posted")


class Trend(BaseModel):
    """A Trend"""

    title: str = Field(description="The title of the trend")
    category: str = Field(description="The category of the trend")
    location: str = Field(description="The location of the trend")
    summary: str = Field(description="The summary of the trend")
    trend_month: date = Field(
        description="The month this trend belongs to in YYYY-MM-DD format."
    )


class FilteredResults(BaseModel):
    filtered_results: list[Result] = Field(description="The list of filtered blogs")


class Trends(BaseModel):
    trends: list[Trend] = Field(description="The list of trends")


class GraphState(TypedDict):
    current_month: date
    raw_trend_results_with_naver_blog: str
    filtered_results: FilteredResults
    scraped_contents: list[str]
    trends: Trends
    is_saved: bool
