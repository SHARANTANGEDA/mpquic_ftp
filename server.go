package main

import (
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"strings"

	quic "github.com/SHARANTANGEDA/mp-quic"
	mpqConstants "github.com/SHARANTANGEDA/mp-quic/constants"

	"github.com/SHARANTANGEDA/mpquic_ftp/common"
	"github.com/SHARANTANGEDA/mpquic_ftp/constants"
)

func main() {
	serverPort, cfgServer := initializeServerArguments()
	serverAddr := constants.SERVER_HOST + ":" + serverPort
	tlsConfig := common.GenerateTLSConfig()
	listener, err := quic.ListenAddr(serverAddr, tlsConfig, cfgServer)
	if err != nil {
		fmt.Println(err)
		fmt.Println("There was an error in socket")
		return
	}
	fmt.Println("Listening on " + serverAddr)
	fmt.Println("Press ^C to shutdown the server")

	for {
		session, err := listener.Accept()
		if err != nil {
			log.Fatal("Error accepting: ", err.Error())
		}
		go performServerActivity(session)
		fmt.Println("Session Started, New Client Spawned")
	}
}

// performServerActivity uses the listener to create new mpQUIC session
// 1. Receive Request Data
// 2. Perform Requested Action
// ==> 2.1 Send File List to client
// ==> 2.2 Send File
func performServerActivity(session quic.Session) {
	var err error
	// 1. Receive Request Data
	dataReceived := common.ReadDataWithQUIC(session)
	requestData := strings.Split(dataReceived, ",")

	// 2. Perform Requested Action
	switch requestData[0] {
	case constants.LIST_FILES_ACTION:
		// 2.1 Send File List to client
		files, err := ioutil.ReadDir(os.Getenv(constants.PROJECT_HOME_DIR) + "/" + constants.SERVER_STORAGE_DIR + "/")
		if err != nil {
			log.Fatal("Error Listing Directory: ", err.Error())
		}

		var fileNameList []string
		for _, f := range files {
			if f.Name() == ".gitkeep" {
				continue
			}
			fileNameList = append(fileNameList, f.Name())
		}

		common.SendStringWithQUIC(session, strings.Join(fileNameList, ","))
	case constants.FILE_FROM_SERVER_ACTION:
		// 2.2 Send File
		err = common.SendFileWithQUIC(session, os.Getenv(constants.PROJECT_HOME_DIR)+"/"+
			constants.SERVER_STORAGE_DIR+"/"+requestData[1])
		if err != nil {
			fmt.Println("Error Sending the file: ", err.Error())
			_ = session.Close(err)
			return
		}

		// Send Ack after file transfer
		common.ReadDataWithQUIC(session)
	case constants.FILE_TO_SERVER_ACTION:
		// 2.2 Receive File
		common.StoreFile(requestData[1], os.Getenv(constants.PROJECT_HOME_DIR)+"/"+constants.SERVER_STORAGE_DIR,
			common.ReadDataWithQUIC(session))

		// Send Ack after file transfer
		common.SendStringWithQUIC(session, constants.CLOSE_CLIENT_GREETING)

	}
	_ = session.Close(err)
}

func initializeServerArguments() (string, *quic.Config) {
	if os.Getenv(constants.PROJECT_HOME_DIR) == "" {
		panic("`PROJECT_HOME_DIR` Env variable not found")
	}

	serverPort := os.Getenv(constants.SERVER_PORT)
	if serverPort == "" {
		panic("`SERVER_PORT` Env variable not found")
	}
	weightsFile := os.Getenv(constants.TRAIN_WEIGHTS_FILE_PARAM)
	if weightsFile == "" {
		panic("`WEIGHTS_FILE_PATH` Env variable not found")
	}

	scheduler := flag.String(constants.SCHEDULER_PARAM, mpqConstants.SCHEDULER_ROUND_ROBIN, "Scheduler Name, a string")
	dumpExperiences := flag.Bool(constants.DUMP_EXPERIENCES_PARAM, false, "a bool(true, false), default: false")
	epsilon := flag.Float64(constants.EPSILON_PARAM, 0.01, "a float64, default: 0 for epsilon value")
	allowedCongestion := flag.Int(constants.ALLOWED_CONGESTION_PARAM, 2500, "a Int, default: 2500")
	flag.Parse()

	return serverPort, &quic.Config{
		WeightsFile:       weightsFile,
		Scheduler:         *scheduler,
		CreatePaths:       true,
		Training:          true,
		DumpExperiences:   *dumpExperiences,
		Epsilon:           *epsilon,
		AllowedCongestion: *allowedCongestion,
	}
}
