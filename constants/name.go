package constants

const (
	// Environment Variables
	SCHEDULER_OUTPUT_DIR = "outputDir"

	SCHEDULER_PARAM          = "scheduler"          // Expect String (Optional)
	UPLOAD_FILE_PARAM        = "file_name"          // Expect String
	ACTION_PARAM             = "action"             // Expect Int
	CREATE_PATHS_PARAM       = "create_paths"       // Expect Bool (Optional)
	TRAIN_WEIGHTS_FILE_PARAM = "weights_file_path"  // Expect String (Optional)
	TRAINING_PARAMS          = "train"              // Expect Bool (Optional)
	EPSILON_PARAM            = "eps"                // Expect Float (Optional)
	ALLOWED_CONGESTION_PARAM = "allowed_congestion" // Expect +ve Int (Optional)
	DUMP_EXPERIENCES_PARAM   = "dump_exp"           // Expect Bool (Optional)
)
