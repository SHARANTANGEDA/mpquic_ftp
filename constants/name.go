package constants

const (
	// Environment Variables
	PROJECT_HOME_DIR         = "PROJECT_HOME_DIR"
	SERVER_IP_ADDRESS        = "SERVER_IP"
	SERVER_PORT              = "SERVER_PORT"
	TRAIN_WEIGHTS_FILE_PARAM = "WEIGHTS_FILE_PATH"

	SCHEDULER_PARAM          = "scheduler"          // Expect String (Optional)
	UPLOAD_FILE_PARAM        = "file_name"          // Expect String
	ACTION_PARAM             = "action"             // Expect Int
	EPSILON_PARAM            = "eps"                // Expect Float (Optional)
	ALLOWED_CONGESTION_PARAM = "allowed_congestion" // Expect +ve Int (Optional)
	DUMP_EXPERIENCES_PARAM   = "dump_exp"           // Expect Bool (Optional)
)
