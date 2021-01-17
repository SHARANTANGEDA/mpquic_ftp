package main

import (
	"crypto/tls"
	"flag"
	"fmt"
	"log"
	"os"
	"strings"

	quic "github.com/SHARANTANGEDA/mp-quic"
	mpqConstants "github.com/SHARANTANGEDA/mp-quic/constants"

	"github.com/SHARANTANGEDA/mpquic_ftp/common"
	"github.com/SHARANTANGEDA/mpquic_ftp/constants"
)

func main() {
	action, fileName, cfgClient := initializeClientArguments()
	tlsConfig := &tls.Config{InsecureSkipVerify: true}
	session, err := quic.DialAddr(constants.SERVER_PUBLIC_ADDRESS+":"+constants.SERVER_PORT, tlsConfig, cfgClient)
	if err != nil {
		log.Fatal("Error connecting to server: ", err.Error())
	}

	if action == "1" {
		// GET File List
		common.SendStringWithQUIC(session, action+",")

		// Receive File List
		fileNameList := strings.Split(common.ReadDataWithQUIC(session), ",")

		// Print File List
		fmt.Println("Available Files: ")
		for idx, file := range fileNameList {
			fmt.Println(idx+1, ": ", file)
		}
	} else {
		// GET File
		common.SendStringWithQUIC(session, action+","+fileName)

		// Receive File
		common.StoreFile(fileName, constants.CLIENT_STORAGE_DIR, common.ReadDataWithQUIC(session))
	}
	_ = session.Close(err)
}

func initializeClientArguments() (string, string, *quic.Config) {
	if os.Getenv(constants.SCHEDULER_OUTPUT_DIR) == "" {
		panic("`outputDir` Env variable not found")
	}

	weightsFile := flag.String(constants.TRAIN_WEIGHTS_FILE_PARAM, "", "Path to weights file, a string, used only for ML based scheduler")
	scheduler := flag.String(constants.SCHEDULER_PARAM, mpqConstants.SCHEDULER_ROUND_ROBIN, "Scheduler Name, a string")
	createPaths := flag.Bool(constants.CREATE_PATHS_PARAM, true, "a bool(true, false), default: true")
	train := flag.Bool(constants.TRAINING_PARAMS, false, "a bool(true, false), default: false")
	dumpExperiences := flag.Bool(constants.DUMP_EXPERIENCES_PARAM, false, "a bool(true, false), default: false")
	epsilon := flag.Float64(constants.EPSILON_PARAM, 0, "a float64, default: 0 for epsilon value")
	allowedCongestion := flag.Int(constants.ALLOWED_CONGESTION_PARAM, 10, "a Int, default: 10")
	action := flag.String(constants.ACTION_PARAM, "1", "1: To Get FileList, 2: Get the file, Default: 1")
	fileName := flag.String(constants.UPLOAD_FILE_PARAM, "", "Mention the fileName, when action is 2 (Required")
	flag.Parse()

	if *action != "1" && *action != "2" {
		log.Fatal("Invalid Action choosen, please choose among 1 or 2")
	}
	if *action == "2" && *fileName == "" {
		log.Fatal("Action 2 requires file_name, please choose file_name")
	}

	return *action, *fileName, &quic.Config{
		WeightsFile:       *weightsFile,
		Scheduler:         *scheduler,
		CreatePaths:       *createPaths,
		Training:          *train,
		DumpExperiences:   *dumpExperiences,
		Epsilon:           *epsilon,
		AllowedCongestion: *allowedCongestion,
	}
}
