"""
Data loading and preprocessing module for video games dashboard.

This module handles automatic loading of the video_games.csv file,
column name normalization, and data validation.
"""

import pandas as pd
import streamlit as st
from typing import Optional


def normalize_column_name(column_name: str) -> str:
    """
    Normalize a column name by replacing dots and spaces with underscores.
    
    Args:
        column_name: Original column name
        
    Returns:
        Normalized column name with dots and spaces replaced by underscores
    """
    return column_name.replace(".", "_").replace(" ", "_")


def load_data(file_path: str = "video_games.csv") -> pd.DataFrame:
    """
    Load video_games.csv from project directory with automatic preprocessing.
    
    This function:
    - Loads the CSV file from the specified path
    - Normalizes column names (replaces dots and spaces with underscores)
    - Validates that the file contains data
    
    Args:
        file_path: Path to the CSV file (default: "video_games.csv")
        
    Returns:
        Cleaned DataFrame with normalized columns
        
    Raises:
        FileNotFoundError: If the CSV file is not found
        ValueError: If the loaded data is empty or invalid
    """
    try:
        # Load the CSV file
        df = pd.read_csv(file_path)
        
        # Validate that we have data
        if df.empty:
            raise ValueError("El archivo CSV está vacío")
        
        # Normalize column names
        df.columns = [normalize_column_name(col) for col in df.columns]
        
        return df
        
    except FileNotFoundError:
        # Provide user-friendly error message in Spanish
        error_msg = f"""
        ❌ **No se encontró el archivo {file_path}**
        
        Por favor, asegúrate de que:
        - El archivo existe en el directorio del proyecto
        - El nombre del archivo es correcto
        - Tienes permisos de lectura para el archivo
        """
        raise FileNotFoundError(error_msg)
    
    except pd.errors.EmptyDataError:
        error_msg = "❌ **El archivo CSV está vacío o no contiene datos válidos**"
        raise ValueError(error_msg)
    
    except Exception as e:
        error_msg = f"❌ **Error al cargar el archivo**: {str(e)}"
        raise Exception(error_msg)


def validate_required_columns(df: pd.DataFrame, required_columns: Optional[list] = None) -> bool:
    """
    Validate that the DataFrame contains required columns.
    
    Args:
        df: DataFrame to validate
        required_columns: List of required column names (after normalization)
                         If None, performs basic validation only
        
    Returns:
        True if validation passes
        
    Raises:
        ValueError: If required columns are missing
    """
    if required_columns is None:
        # Basic validation - just check we have some columns
        if len(df.columns) == 0:
            raise ValueError("El DataFrame no contiene columnas")
        return True
    
    # Check for required columns
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        error_msg = f"""
        ❌ **Faltan columnas requeridas**: {', '.join(missing_columns)}
        
        Columnas disponibles: {', '.join(df.columns.tolist())}
        """
        raise ValueError(error_msg)
    
    return True


def find_column(df: pd.DataFrame, options: list) -> Optional[str]:
    """
    Find the first matching column from a list of options.
    
    This is a helper function for flexible column detection when
    column names might vary.
    
    Args:
        df: DataFrame to search
        options: List of possible column names to look for
        
    Returns:
        First matching column name, or None if no match found
    """
    for option in options:
        if option in df.columns:
            return option
    return None
