"""
Módulo de procesamiento de datos

Contiene clases y funciones para cargar, preprocesar y gestionar
los datasets de actos administrativos.
"""

from .data_loader import DataLoader
from .preprocessor import TextPreprocessor
from .dataset import ActosDataset

__all__ = ['DataLoader', 'TextPreprocessor', 'ActosDataset']
