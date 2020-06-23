import langid

def get_language_of_text(txt):
    return langid.classify(str(txt))[0]

def get_language_from_column(df_col_txt, nb_rows, recipe_params):  
    if len(recipe_params["constrain_languages"]) > 0:
        langid.set_languages(recipe_params["constrain_languages"])  
    # the df[col_lang] if filled with the language name
    if recipe_params["detect_language"]:
        if recipe_params["single_language_per_column"]:
            # check language on the 10000 first cells of the text column
            lang = get_language_of_text(str(df_col_txt[:10000]))
            return [lang]*nb_rows
        else:
            return df_col_txt.apply(lambda x: get_language_of_text(x[:500]))
    else:
        # Enven though the language is given in the UI, language column is created for the sake of code consistency
        return [recipe_params["language"]]*nb_rows
    