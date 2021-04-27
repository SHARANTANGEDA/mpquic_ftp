package constants

const (
	// Environment Variables
	PROJECT_HOME_DIR         = "PROJECT_HOME_DIR"
	SERVER_IP_ADDRESS        = "SERVER_IP"
	SERVER_PORT              = "SERVER_PORT"
	TRAIN_WEIGHTS_FILE_PARAM = "WEIGHTS_FILE_PATH"

	SCHEDULER_PARAM          = "scheduler"          // Expect String (Optional)
	DOWNLOAD_FILE_PARAM      = "file_name"          // Expect String
	UPLOAD_FILE_PATH_PARAM   = "file_path"          // Absolute path as String
	ACTION_PARAM             = "action"             // Expect Int
	EPSILON_PARAM            = "eps"                // Expect Float (Optional)
	ALLOWED_CONGESTION_PARAM = "allowed_congestion" // Expect +ve Int (Optional)
	DUMP_EXPERIENCES_PARAM   = "dump_exp"           // Expect Bool (Optional)
	BANDWIDTH_1_PARAM        = "bw_1"               // Expect Float
	BANDWIDTH_2_PARAM        = "bw_2"               // Expect Float
	DELAY_1_PARAM            = "delay_1"            // Expect Float
	DELAY_2_PARAM            = "delay_2"            // Expect Float
	LOSS_1_PARAM             = "loss_1"             // Expect Float
	LOSS_2_PARAM             = "loss_2"             // Expect Float
	SPLIT_RATIO_PARAM        = "split_ratio"        // Expect Float

	LIST_FILES_ACTION       = "1"
	FILE_FROM_SERVER_ACTION = "2"
	FILE_TO_SERVER_ACTION   = "3"
)
