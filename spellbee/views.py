import json 

from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from spellbee.utils_session import generate_session_id
from spellbee.utils import (load_pangram_data, 
                            get_all_words, 
                            get_alphabet_weights, 
                            generate_letters_for_spellbee,
                            is_valid_word,
                            score_word   ,
                            check_duplicate               
)
from spellbee.score_data import scores

pangram = load_pangram_data()
all_words = get_all_words()  # All words that don't contain letter "s"
alphabet_weights = get_alphabet_weights()


class RefreshLetters(APIView):
    """ Refreshes the letter being generated """

    def get(self, request, format=None):
        try:
            choice, outer_letters, inner_letter = generate_letters_for_spellbee(pangram, alphabet_weights)
            data = {
                # 'choice': choice,
                'outer' : list(outer_letters),
                'inner' : inner_letter
            }
            return JsonResponse(data, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': f"Error Fetching letters {e}"}, status=status.HTTP_400_BAD_REQUEST)



class ValidateInput(APIView):
    """  Validates and scores the user input word """

    def post(self, request, format=None):
            # Expected request: {
            # "input_word": "word",
            # "current_score" : 10,
            # "inner_letter": "inner_letter",
            # "outer_letters": "outer_letters",
            # }

        try:
            data = request.data
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid Json data in request body"}, status=status.HTTP_400_BAD_REQUEST)

        word = data.get("input_word", "")
        current_score = int(data.get("current_score", 0))
        inner_letter = data.get("inner_letter", "")
        outer_letters = data.get("outer_letters", [])


        is_valid = is_valid_word(word, inner_letter, outer_letters)
        new_total_score = score_word(word, current_score)

        if not is_valid:
            new_total_score = current_score

        response = {
            "is_valid": is_valid,
            "new_total_score" : new_total_score,
        }
        return JsonResponse(response, status=status.HTTP_200_OK)


