package controller

import (
	"fmt"
	"io"
	"log"
	"net/http"

	"github.com/gin-gonic/gin"
	authpb "github.com/snapser/gin-grpc/snapserpb/auth"
	eventbuspb "github.com/snapser/gin-grpc/snapserpb/eventbus"
	inventorypb "github.com/snapser/gin-grpc/snapserpb/inventory"
	"google.golang.org/protobuf/encoding/protojson"
	"google.golang.org/protobuf/proto"
	"google.golang.org/protobuf/reflect/protoreflect"
)

// POST debug/echo is an endpoint that simply prints the body of the request and returns a 200 status
// it also logs the body to stdout
func (ps *PostgameServer) Events(c *gin.Context) {
	body, err := io.ReadAll(c.Request.Body)
	if err != nil {
		panic(err)
	}
	r := c.Request

	fmt.Printf("%s %s\n", r.Method, r.URL.Path)
	fmt.Printf("Content-Type: %s\n", r.Header.Get("Content-Type"))

	// Parse body as eventbus.WebhookMessage
	var wr eventbuspb.ByoWebhookRequest
	err = proto.Unmarshal(body, &wr)
	if err != nil {
		// Log the body
		fmt.Printf("Body: %s\n", body)
		panic(err)
	}

	// Switch on the message type - only one right now which is SNAP_EVENT
	switch wr.MessageType {
	case eventbuspb.MessageType_MESSAGE_TYPE_SNAP_EVENT:
		snapEvent := wr.GetByoSnapEvent()
		// Switch on the service_name to know which enum to use for the event-type -> message-type
		switch snapEvent.ServiceName {
		case "auth":
			// Switch on the event-id (the Event* enums in each service types proto)
			switch snapEvent.EventId {
			case uint32(authpb.AuthEventType_AUTH_ANON_USER_ADDED):
				authAnonUserAdded := &authpb.EventAuthAnonUserAdded{}
				if err := proto.Unmarshal([]byte(snapEvent.Payload), authAnonUserAdded); err != nil {
					panic(err)
				}
				fmt.Printf("Got EventAuthAnonUserAdded: %v\n", authAnonUserAdded)
				PrintMessage(authAnonUserAdded)
			default:
				log.Printf("unknown event_id: %v", snapEvent.EventId)
			}
		case "inventory":
			switch snapEvent.EventId {
			case uint32(inventorypb.InventoryEventType_INVENTORY_ITEM_ADDED):
				ev := &inventorypb.EventInventoryItemAdded{}
				if err := proto.Unmarshal([]byte(snapEvent.Payload), ev); err != nil {
					panic(err)
				}
				fmt.Printf("Got EventInventoryItemAdded: %v\n", ev)
				PrintMessage(ev)
			case uint32(inventorypb.InventoryEventType_INVENTORY_ITEM_CONSUMED):
				ev := &inventorypb.EventInventoryItemConsumed{}
				if err := proto.Unmarshal([]byte(snapEvent.Payload), ev); err != nil {
					panic(err)
				}
				fmt.Printf("Got EventInventoryItemConsumed: %v\n", ev)
				PrintMessage(ev)
			case uint32(inventorypb.InventoryEventType_INVENTORY_ITEM_PURCHASED):
				ev := &inventorypb.EventInventoryItemPurchased{}
				if err := proto.Unmarshal([]byte(snapEvent.Payload), ev); err != nil {
					panic(err)
				}
				fmt.Printf("Got EventInventoryItemPurchased: %v\n", ev)
				PrintMessage(ev)
			case uint32(inventorypb.InventoryEventType_INVENTORY_CURRENCY_BALANCE_UPDATED):
				ev := &inventorypb.EventInventoryCurrencyBalanceUpdated{}
				if err := proto.Unmarshal([]byte(snapEvent.Payload), ev); err != nil {
					panic(err)
				}
				fmt.Printf("Got EventInventoryCurrencyBalanceUpdated: %v\n", ev)
				PrintMessage(ev)
			default:
				log.Printf("unknown service_name: %v", snapEvent.ServiceName)
			}
		}
	default:
		log.Printf("unhandled message type: %v", wr.MessageType)
	}

	c.Writer.WriteHeader(http.StatusOK)
	c.Writer.Write([]byte("ok"))
}

// PrintMessage takes a proto.Message and prints it as pretty-printed json
func PrintMessage(msg protoreflect.ProtoMessage) {
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
