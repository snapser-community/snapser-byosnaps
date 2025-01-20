package main

import (
	"math/rand"
)

type PraiseResponse struct {
	Quote string `json:"quote"`
}

var fallbackPraises = []string{
	"You're doing amazing work!",
	"Keep up the fantastic effort!",
	"Your dedication is inspiring!",
	"You're a star, keep shining!",
	"You have the power to achieve great things!",
	"Believe in yourself, you're unstoppable!",
}

func getRandomPraise() string {
	return fallbackPraises[rand.Intn(len(fallbackPraises))]
}
