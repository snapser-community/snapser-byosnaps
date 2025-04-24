package main

import (
	"fmt"
	"io"
	"net/http"

	"math/rand"

	"github.com/gin-gonic/gin"
	"github.com/rs/zerolog"
	eventbuspb "github.com/snapser-community/snapser-byosnaps/byosnap-go/snapserpb/eventbus"
	lobbiespb "github.com/snapser-community/snapser-byosnaps/byosnap-go/snapserpb/lobbies"
	"google.golang.org/grpc/metadata"
	"google.golang.org/protobuf/proto"
)

func (a *app) eventHandler(c *gin.Context) {
	ctx := c.Request.Context()
	log := zerolog.Ctx(c.Request.Context())

	// Read the body in as a byte slice
	body, err := io.ReadAll(c.Request.Body)
	if err != nil {
		log.Fatal().Err(err).Msg("failed to read body")
	}

	// 👇 Parse body as eventbus.ByoWebhookMessage
	var wr eventbuspb.ByoWebhookRequest
	err = proto.Unmarshal(body, &wr)
	if err != nil {
		log.Fatal().Str("requestBody", string(body)).Err(err).Msg("failed to unmarshal body")
	}

	// Switch on the message type
	// NOTE: Currently the only type we handle is snap events
	switch wr.MessageType {
	case eventbuspb.MessageType_MESSAGE_TYPE_SNAP_EVENT:
		snapEvent := wr.GetByoSnapEvent()
		log.Debug().Interface("snapEvent", snapEvent).Msg("received snap event")

		// Switch on the subject which is the recommended way to identify the event and payload
		switch snapEvent.Subject {
		//👇 For this tutorial we are going to listen on a Lobby member joined event
		case "snapser.services.lobbies.member.joined":
			ev := &lobbiespb.EventLobbiesMemberJoined{}
			if err := proto.Unmarshal([]byte(snapEvent.Payload), ev); err != nil {
				panic(err)
			}
			log.Info().Msgf("got EventLobbiesMemberJoined: %v", ev)

			// Some praise messages
			var fallbackPraises = []string{
				"You're doing amazing work!",
				"Keep up the fantastic effort!",
				"Your dedication is inspiring!",
				"You're a star, keep shining!",
				"You have the power to achieve great things!",
				"Believe in yourself, you're unstoppable!",
			}

			randomPraise := fallbackPraises[rand.Intn(len(fallbackPraises))]
			//👇 After, getting this event we are going to emit the custom Praise event we registered
			praiseReq := &eventbuspb.PublishByoEventRequest{
				ByosnapId:  byoSnapID,
				Subject:    "praise",
				Payload:    []byte(fmt.Sprintf("Nice work, you joined a lobby - %s", randomPraise)),
				Recipients: []string{ev.JoinedUserId},
			}
			ctx = metadata.NewOutgoingContext(ctx, metadata.Pairs("gateway", "internal"))
			_, err := a.eventbusClient.PublishByoEvent(ctx, praiseReq)
			if err != nil {
				log.Error().Err(err).Msg("failed to publish event")
			} else {
				log.Info().Msgf("published praise event: %v", praiseReq)
			}
		default:
			log.Warn().Msgf("unhandled event: [eventTypeId=%d, subject=%s, serviceName=%s]",
				snapEvent.EventTypeId, snapEvent.Subject, snapEvent.ServiceName)
		}
	default:
		log.Printf("unhandled message type: %v", wr.MessageType)
	}

	c.Writer.WriteHeader(http.StatusOK)
	c.Writer.Write([]byte("ok"))
}
