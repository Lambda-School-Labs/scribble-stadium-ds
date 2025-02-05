import logging

from fastapi import APIRouter

from app.api.models import HistogramRequest, LineGraphRequest, CroppedWordsRequest, CropCloudRequest
from app.utils.visualizations import histogram, line_graph, crop_cloud

# global variables and services
router = APIRouter()
log = logging.getLogger(__name__)

# New experiment
import os
from dotenv import load_dotenv
from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader

@router.post("/viz/linegraph")
def return_line_graph(data: LineGraphRequest):
    """Endpoint produces a line graph of student's SquadScore history.

    Arguments
    ---
    `ScoreHistory` list - list with history of squadscores for current period

    `StudentName` str - String containing the student's first name

    Returns:
    ---
    `response` json - A graph object produced by Plotly.Graph.to_json() function

    Note:
    ---
    All submissions that are included in this data are post moderation review
    and Approved for COPPA compliance
    """
    return line_graph.line_graph(data.ScoreHistory, data.StudentName)


@router.post("/viz/histogram")
def return_histogram(data: HistogramRequest):
    """Endpoint that makes Plotly histogram of current grade's SquadScore
    distribution for the current period. Graph is annotated with a vertical line
    representing the student's most recent score that has passed the moderation
    phase of submission processing.

    Arguments:
    ---
    `GradeList` list - list containing the other student's scores from this week

    `GradeLevel` int - Current grade level for student

    `StudentName` str - String containing the student's first name

    `StudentScore` float - current student's submission score

    Returns:
    ---
    `response` json - A graph object produced by Plotly.Graph.to_json() function

    Note:
    ---
    All submissions that are included in this data are post moderation review
    and Approved for COPPA compliance
    """
    return histogram.histogram(
        data.GradeList, [data.GradeLevel, data.StudentName, data.StudentScore]
    )

@router.post("/viz/cropped_words")
def get_cropped_words(data: CroppedWordsRequest):
    """Endpoint produces a crop cloud of the student's progression in handwritting over time.

    Arguments
    ---
    `user_id` str - a string containing the user_id

    `date_range` List[str] - a list of two dates in the format of YYYY-MM-DD

    `complexity_metric` str - how to calculate the complexity of words (from 'len', 'syl', 'len_count', 'syl_count')

    `image_format` str - the format of the cropped word images (from '.png', '.webp', or anything OpenCV supports)

    `canvas_area` int - the area of the canvas in pixels

    `density` float - the bounding box area of the cropped words divided by the canvas area

    Returns:
    ---
    `response` json(csv([width, height, text, page_uri, date, complexity, image_base64])) - a table of the cropped words

    Note:
    ---
    All submissions that are included in this data are pre moderation review
    and not Approved for COPPA compliance
    """
    return crop_cloud.get_cropped_words(
        user_id=data.user_id,
        date_range=data.date_range,
        complexity_metric=data.complexity_metric,
        image_format=data.image_format,
        canvas_area=data.canvas_area,
        density=data.density,
        )

@router.post("/viz/crop_cloud")
def get_crop_cloud(data: CropCloudRequest):
    """Endpoint produces a crop cloud of the student's progression in handwritting over time.

    Arguments
    ---
    `user_id` str - a string containing the user_id. Choices are "Chickpea", "Holmes", "XiChi", "YoungBlood", "PenDragon", "Frogurt"

    `date_range` List[str] - a list of two dates in the format of YYYY-MM-DD. Submissions were randomly generated between 2015-01-01 and 2021-12-31

    `complexity_metric` str - how to calculate the complexity of words (from 'len', 'syl', 'len_count', 'syl_count')

    `image_format` str - the format of the cropped word images (from '.png', '.webp', or anything OpenCV supports)

    `canvas_width` int - the width of the crop cloud in pixels

    `density` float - the bounding box area of the cropped words divided by the canvas area

    `max_words` int - the max number of words to include in the cloud

    Returns:
    ---
    `response` json(image_base64) - a rendered crop cloud as an image

    Note:
    ---
    All submissions that are included in this data are pre moderation review
    and not Approved for COPPA compliance
    """
    return crop_cloud.get_crop_cloud(
        user_id=data.user_id,
        date_range=data.date_range,
        complexity_metric=data.complexity_metric,
        image_format=data.image_format,
        canvas_width=data.canvas_width,
        density=data.density,
        max_words=data.max_words,
        )
