package main

import (
	"fmt"
	"io"
	"log/slog"
	"net/http"

	"math/rand"

	"github.com/gin-gonic/gin"
	eventbuspb "github.com/snapser-community/snapser-byosnaps/byosnap-go/snapserpb/eventbus"
	lobbiespb "github.com/snapser-community/snapser-byosnaps/byosnap-go/snapserpb/lobbies"
	"google.golang.org/protobuf/proto"
)

func (a *app) eventHandler(c *gin.Context) {
	ctx := c.Request.Context()
	// 👇 Logger bound by the requestLogging middleware: every line below carries
	// the request-id of this webhook delivery.
	log := requestLogger(c.Request)

	// Read the body in as a byte slice
	body, err := io.ReadAll(c.Request.Body)
	if err != nil {
		log.Error("failed to read body", slog.Any("error", err))
		c.Status(http.StatusBadRequest)
		return
	}

	// 👇 Parse body as eventbus.ByoWebhookMessage
	var wr eventbuspb.ByoWebhookRequest
	err = proto.Unmarshal(body, &wr)
	if err != nil {
		log.Error("failed to unmarshal body",
			slog.String("requestBody", string(body)), slog.Any("error", err))
		c.Status(http.StatusBadRequest)
		return
	}

	// Switch on the message type
	// NOTE: Currently the only type we handle is snap events
	switch wr.MessageType {
	case eventbuspb.MessageType_MESSAGE_TYPE_SNAP_EVENT:
		snapEvent := wr.GetByoSnapEvent()
		log.Debug("received snap event", slog.Any("snapEvent", snapEvent))

		// Switch on the subject which is the recommended way to identify the event and payload
		switch snapEvent.Subject {
		//👇 For this tutorial we are going to listen on a Lobby member joined event
		case "snapser.services.lobbies.member.joined":
			ev := &lobbiespb.EventLobbiesMemberJoined{}
			if err := proto.Unmarshal([]byte(snapEvent.Payload), ev); err != nil {
				log.Error("failed to unmarshal lobby member joined payload", slog.Any("error", err))
				break
			}
			log.Info("got EventLobbiesMemberJoined", slog.Any("event", ev))

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
			// 👇 outgoingInternalContext forwards the x-request-id metadata, so the
			// Eventbus logs this publish under the same request-id.
			_, err := a.eventbusClient.PublishByoEvent(outgoingInternalContext(ctx), praiseReq)
			if err != nil {
				log.Error("failed to publish event", slog.Any("error", err))
			} else {
				log.Info("published praise event", slog.String("subject", praiseReq.Subject))
			}
		default:
			log.Warn("unhandled event",
				slog.Uint64("eventTypeId", uint64(snapEvent.EventTypeId)),
				slog.String("subject", snapEvent.Subject),
				slog.String("serviceName", snapEvent.ServiceName))
		}
	default:
		log.Warn("unhandled message type", slog.String("messageType", wr.MessageType.String()))
	}

	c.Writer.WriteHeader(http.StatusOK)
	c.Writer.Write([]byte("ok"))
}
