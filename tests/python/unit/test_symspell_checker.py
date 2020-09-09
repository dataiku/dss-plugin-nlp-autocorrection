# -*- coding: utf-8 -*-
# This is a test file intended to be used with pytest
# pytest automatically runs all the function starting with "test_"
# see https://docs.pytest.org for more information

import os
import pandas as pd

from symspell_checker import SpellChecker  # noqa

dictionary_folder_path = os.getenv("DICTIONARY_FOLDER_PATH")


def test_spellcheck_df_english():
    input_df = pd.DataFrame(
        {"input_text": ["Can yu read tHISs message despite the horible AB1234 sppeling msitakes 😂 #OMG"]}
    )
    spellchecker = SpellChecker(dictionary_folder_path)
    output_df = spellchecker.check_df(df=input_df, text_column="input_text", language="en")
    corrected_text_column = list(spellchecker._output_column_description_dict.keys())[0]
    corrected_text = output_df[corrected_text_column][0]
    expected_correction = "Can you read tHIS message despite the horrible AB1234 spelling mistakes 😂 #OMG"
    assert corrected_text == expected_correction


def test_spellcheck_df_multilingual():
    input_df = pd.DataFrame(
        {
            "input_text": [
                "Can yu read tHISs message despite the horible AB1234 sppeling msitakes 😂 #OMG",
                "Les fautes d'orthografe c pas toop #LOOOL PTDR",
                "Toodo lo que puéde ser covfefe es real.",
            ],
            "language": ["en", "fr", "es"],
        }
    )
    spellchecker = SpellChecker(dictionary_folder_path, custom_vocabulary_set={"PTDR"})
    output_df = spellchecker.check_df(df=input_df, text_column="input_text", language_column="language")
    corrected_text_column = list(spellchecker._output_column_description_dict.keys())[0]
    corrected_texts = output_df[corrected_text_column].values.tolist()
    expected_corrections = [
        "Can you read tHIS message despite the horrible AB1234 spelling mistakes 😂 #OMG",
        "Les fautes d'orthographe c pas trop #LOOOL PTDR",
        "Todo lo que puede ser covfefe es real.",
    ]
    assert corrected_texts == expected_corrections
