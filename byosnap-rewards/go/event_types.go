package main

import (
	"fmt"

	eventbuspb "github.com/snapser-community/snapser-byosnaps/byosnap-rewards/snapserpb/eventbus"
)

// Praise reward, a message praising the player for doing something
var praiseEventType = &eventbuspb.SnapserEventType{
	Subject:            fmt.Sprintf("snapser.byo.%s.praise", byoSnapID),
	Description:        "Praise the user for doing something",
	MessageType:        "rewards.Praise",
	EventTypeEnumValue: 1,
}

var eventTypes = []*eventbuspb.SnapserEventType{
	praiseEventType,
}
