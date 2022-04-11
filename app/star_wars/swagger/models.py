"""Swagger models"""
from doctest import Example
from flask_restx import Model, fields

skywalker = Model(
    "skywalker",
    {
        "status": fields.Integer(
            description="Request status code",
            required=True,
            example=200
        ),
        "description": fields.String(
            description="Skywalker's lore",
            required=True,
            example="Luke Skywalker participated in A New Hope, The Empire Strikes Back, Return of the Jedi and Revenge of the Sith. Anakin Skywalker participated in The Phantom Menace, Attack of the Clones and Revenge of the Sith. Shmi Skywalker participated in The Phantom Menace and Attack of the Clones."
        )
    }  
)
