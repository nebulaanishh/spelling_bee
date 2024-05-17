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
                            score_word                  
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
        # "session_id": "session_id",
        # }

        try:
            data = request.data
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid Json data in request body"}, status=status.HTTP_400_BAD_REQUEST)
        

        word = data.get("input_word", "")
        session_id = data.get("session_id", generate_session_id())

        is_valid = is_valid_word(word, session_id)
        score = score_word(word, session_id)

        response = {
            "is_valid": is_valid,
            "total_score" : score,
            "is_duplicate": False,
        }



        return JsonResponse(response, status=status.HTTP_200_OK)




class InitializeSession(APIView):
    """ """

    def get(self, request, format=None):
        # Call initialize function

        response = {}
        return JsonResponse(response, status=status.HTTP_200_OK)