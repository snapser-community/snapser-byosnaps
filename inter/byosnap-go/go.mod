module byosnap-go

go 1.21.13

replace snapser_internal => ./snapser_internal

require (
	github.com/gorilla/handlers v1.5.2
	github.com/gorilla/mux v1.8.1
	snapser_internal v0.0.0-00010101000000-000000000000
)

require github.com/felixge/httpsnoop v1.0.3 // indirect
