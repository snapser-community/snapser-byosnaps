package main

import (
	"context"
	"fmt"
	"io"
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/rs/zerolog"
	authpb "github.com/snapser/byosnap-rewards/snapserpb/auth"
	eventbuspb "github.com/snapser/byosnap-rewards/snapserpb/eventbus"
	lobbiespb "github.com/snapser/byosnap-rewards/snapserpb/lobbies"
	"google.golang.org/grpc/metadata"
	"google.golang.org/protobuf/encoding/protojson"
	"google.golang.org/protobuf/proto"
	"google.golang.org/protobuf/reflect/protoreflect"
)

func (a *app) eventHandler(c *gin.Context) {
	ctx := c.Request.Context()
	log := zerolog.Ctx(c.Request.Context())

	body, err := io.ReadAll(c.Request.Body)
	if err != nil {
		panic(err)
	}

	// Parse body as eventbus.WebhookMessage
	var wr eventbuspb.ByoWebhookRequest
	err = proto.Unmarshal(body, &wr)
	if err != nil {
		// Log the body
		fmt.Printf("Body: %s\n", body)
		panic(err)
	}

	// Switch on the message type
	switch wr.MessageType {
	case eventbuspb.MessageType_MESSAGE_TYPE_SNAP_EVENT:
		snapEvent := wr.GetByoSnapEvent()

		// Switch on the service_name to know which enum to use for the event-type -> message-type
		switch snapEvent.ServiceName {
		case byoSnapID:
			log.Info().Msgf("Received %s event: %v", byoSnapID, snapEvent)

		case "auth":
			// Switch on the event-id (the Event* enums in each service types proto)
			switch snapEvent.EventId {
			case uint32(authpb.AuthEventType_AUTH_ANON_USER_ADDED):
				authAnonUserAdded := &authpb.EventAuthAnonUserAdded{}
				if err := proto.Unmarshal([]byte(snapEvent.Payload), authAnonUserAdded); err != nil {
					panic(err)
				}
				fmt.Printf("Got EventAuthAnonUserAdded: %v\n", authAnonUserAdded)
				PrintMessage(ctx, authAnonUserAdded)
			default:
				log.Printf("unknown event_id: %v", snapEvent.EventId)
			}
		case "lobbies":
			switch snapEvent.EventId {
			case uint32(lobbiespb.LobbiesEventType_LOBBIES_MEMBER_JOINED):
				ev := &lobbiespb.EventLobbiesMemberJoined{}
				if err := proto.Unmarshal([]byte(snapEvent.Payload), ev); err != nil {
					panic(err)
				}
				log.Info().Msgf("got EventLobbiesMemberJoined: %v", ev)

				// Praise the user
				// Publish our custom event using evntbus publish
				payload := []byte(fmt.Sprintf("Nice work, you joined a lobby - %s", getRandomPraise()))

				praiseReq := &eventbuspb.PublishEventRequest{
					ServiceName: byoSnapID,
					Subject:     "praise",
					EventTypeId: praiseEventType.EventTypeEnumValue,
					Payload:     payload,
					Recipients:  []string{ev.JoinedUserId},
				}
				md := metadata.Pairs("gateway", "internal")
				ctx = metadata.NewOutgoingContext(ctx, md)
				_, err := a.eventbusClient.PublishEvent(ctx, praiseReq)
				if err != nil {
					log.Error().Err(err).Msg("failed to publish event")
				} else {
					log.Info().Msgf("published praise event: %v", praiseReq)
				}
			default:
				log.Info().Msgf("unhandled lobbies event_id: %v", snapEvent.EventId)
			}
		}
	default:
		log.Printf("unhandled message type: %v", wr.MessageType)
	}

	c.Writer.WriteHeader(http.StatusOK)
	c.Writer.Write([]byte("ok"))
}

// PrintMessage takes a proto.Message and prints it as pretty-printed json
func PrintMessage(ctx context.Context, msg protoreflect.ProtoMessage) {
	log := zerolog.Ctx(ctx)
	marshaller := protojson.MarshalOptions{
		Multiline: true,
		Indent:    "  ",
	}
	json, err := marshaller.Marshal(msg)
	if err != nil {
		log.Printf("Error marshalling message: %v", err)
		return
	}
	fmt.Printf("%T as JSON:\n%v\n", msg, string(json))
}
